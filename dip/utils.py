import json

from django.core import serializers
from django.db.models import QuerySet, Model
from django.utils import timezone
from ipphone_app.models import Log
import inspect
import traceback


class LogManager:
    log_messages = {
        # Определите ваши собственные сообщения логов здесь
        "unexpected_error": {
            "msg": "An unexpected error occurred: {error_detail}",
            "type": "error",
        },
        "login": {"msg": "Пользователь {user} авторизовался"},
        "create": {"msg": "У {model} было создано запись"},
        "update": {"msg": "У {model} было обновлено запись"},
        "delete": {"msg": "У {model} было удалено запись"},
        "action": {"msg": "Было сделано действие {action}"},
    }

    @classmethod
    def get_log_msg(cls, slug, **kwargs):
        """
        Возвращает лог-сообщение для заданного ключа (slug).
        kwargs позволяет динамически добавлять данные в сообщение.
        """
        provided_fields = " | ".join(
            [f"{key}: {value}" for key, value in kwargs.items()]
        )

        log_data = cls.log_messages.get(
            slug,
            {
                "msg": f"Unknown log error, provided fields: {provided_fields}",
                "type": "error",
            },
        )

        try:
            msg = log_data["msg"].format(**kwargs)
            msg_type = "success"
        except Exception as e:
            msg = (
                f"{log_data['msg']}, but an error occurred during formatting the log message. "
                f"Provided fields: {provided_fields}. Slug: {slug}"
            )
            msg_type = "error_logging"

        return msg, msg_type

    @classmethod
    def __do_log(
        cls, slug, by_user_id=None, prev_values=None, next_values=None, **kwargs
    ):
        try:
            # Получаем сообщение и тип лога
            message, log_type = cls.get_log_msg(slug, **kwargs)
            Log.objects.create(
                by_user_id=by_user_id,
                text=message,
                prev_values=prev_values,
                next_values=next_values,
                slug=slug,
                status=log_type,
                logged_in_code=inspect.stack()[
                    2
                ].function,  # Исправлено на [2] для корректного уровня стека
                created_at=timezone.now(),
            )
        except Exception as e:
            cls._log_unexpected_error(e, by_user_id)

    @classmethod
    def __do_req_log(cls, request, slug, prev_values=None, next_values=None, **kwargs):
        try:
            by_user_id = None
            requested_path = None
            request_method = None

            if request and hasattr(request, "user"):
                by_user_id = request.user.id if request.user.is_authenticated else None
            else:
                # Если request не предоставлен или не имеет пользователя, используем __do_log без request
                cls.__do_log(slug=slug, **kwargs)
                return  # Выходим после логирования

            if request and hasattr(request, "path"):
                requested_path = request.path

            if request and hasattr(request, "method"):
                request_method = request.method

            # Получаем сообщение и тип лога
            message, log_type = cls.get_log_msg(slug, **kwargs)
            if requested_path:
                message += f" <br>| requested path: {requested_path}"
            if request_method:
                message += f" <br>| request method: {request_method}"
            Log.objects.create(
                by_user_id=by_user_id,
                text=message,
                prev_values=prev_values,
                next_values=next_values,
                slug=slug,
                status=log_type,
                logged_in_code=inspect.stack()[
                    2
                ].function,  # Исправлено на [2] для корректного уровня стека
                created_at=timezone.now(),
            )
        except Exception as e:
            # Автоматически логируем неожиданные ошибки, если логирование само по себе не удалось
            cls._log_unexpected_error(
                e, request.user.id if request.user.is_authenticated else None
            )

    @classmethod
    def data_to_json(cls, data):
        if not data:
            return None
        if isinstance(data, QuerySet):
            data = serializers.serialize("json", data)
        elif isinstance(data, Model):
            data = serializers.serialize("json", [data])
        else:
            # If it's not a QuerySet, wrap it in a list and serialize
            data = json.dumps(data)
        return data

    @classmethod
    def make_log(
        cls,
        request=None,
        slug=None,
        by_user_id=None,
        prev_values=None,
        next_values=None,
        **kwargs,
    ):
        """
        Универсальный метод для логирования. Если request предоставлен, использует __do_req_log,
        иначе использует __do_log.
        """
        # сериализируем данные на json
        prev_values = cls.data_to_json(prev_values)
        next_values = cls.data_to_json(next_values)

        if slug is None:
            slug = "unknown_error"

        if request is not None:
            cls.__do_req_log(request, slug, prev_values, next_values, **kwargs)
        else:
            cls.__do_log(
                slug,
                by_user_id=by_user_id,
                prev_values=prev_values,
                next_values=next_values,
                **kwargs,
            )

    @classmethod
    def _log_unexpected_error(cls, error, by_user_id=None):
        """
        Обрабатывает неожиданные ошибки путем логирования их с упрощенным трассбеком.
        error - исключение, которое было вызвано.
        """
        # Захватываем полный трассбек
        full_traceback = traceback.format_exc()

        # Разбиваем трассбек на отдельные строки
        traceback_lines = full_traceback.strip().split("\n")

        # Извлекаем первую и последнюю строки трассбека
        if len(traceback_lines) > 1:
            first_line = traceback_lines[0]
            last_line = traceback_lines[-1]
            simplified_traceback = (
                f"{first_line}\n... (traceback omitted) ...\n{last_line}"
            )
        else:
            simplified_traceback = (
                traceback_lines[0] if traceback_lines else "No traceback available"
            )

        # Подготавливаем детали ошибки с упрощенным трассбеком
        error_detail = f"{str(error)}; Traceback: {simplified_traceback}"

        # Логируем ошибку с упрощенным трассбеком
        Log.objects.create(
            text=f"Unexpected error during logging: {error_detail}",
            slug="unexpected_error",
            by_user_id=by_user_id,
            status="error",
            logged_in_code="_log_unexpected_error",
            created_at=timezone.now(),
        )
