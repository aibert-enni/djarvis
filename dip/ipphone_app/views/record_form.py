import copy
import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic.edit import FormView, UpdateView
from django.views import View
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.core.cache import cache
import json

from ipphone_app.models import Record, Token, RecordFormConfiguration
from ipphone_app.forms import (
    UpdateRecordForm,
    RecordFormConfigurationForm,
)
from ipphone_app.utils import check_token
from utils import LogManager


class RecordUpdateFormView(FormView):
    model = Record
    form_class = UpdateRecordForm
    template_name = "update_form/record_update_form.html"

    def dispatch(self, request, *args, **kwargs):
        config = RecordFormConfiguration.get_active_config()
        if not config.is_active:
            return HttpResponseForbidden("Ссылка на данный момент не работает, обратитесь в 516")
        token = kwargs.get("token")
        token = check_token(token)
        if not token:
            return HttpResponseForbidden(
                "Вы уже поменяли данные или данная ссылка устарела, обратитесь в 516"
            )
        token.attempt_decrement()
        token.save()
        if not token.is_valid():
            return HttpResponseForbidden(
                "Вы уже поменяли данные или данная ссылка устарела, обратитесь в 516"
            )
        self.object = token.record
        self.old_object = copy.deepcopy(self.object) # to save previous data of record in logs
        self.token = token
        return super().dispatch(request, *args, **kwargs)

    # init form
    def get_form(self, form_class=None):
        form = self.form_class(
            self.request.POST or None, self.request.FILES or None, instance=self.object
        )
        token = self.token
        permission_fields = [
            "phone",
            "full_name",
            "department",
            "position",
            "room",
            "email",
            "image",
        ]
        for field in permission_fields:
            if not getattr(token, field):
                form.fields[field].disabled = True
            form.fields[field].initial = getattr(self.object, field)
        return form

    def form_valid(self, form):
        prev_record = self.old_object
        record = form.save()
        LogManager.make_log(
            request=self.request,
            slug="update",
            prev_values=prev_record,
            next_values=record,
            model="Record",
        )
        messages.success(self.request, "Ваши данные были обновлены")
        return redirect("home")


class SendRecordsFormsView(View):
    template_name = "update_form/record_update_links.html"

    @transaction.atomic
    def post(self, request):
        config = RecordFormConfiguration.objects.get(pk=1)
        if not config.is_active:
            message = "Формы отключены, надо включить в настройках рассылки что бы они работали"
            return JsonResponse(
                {
                    "form_html": "",
                    "message": message,
                }
            )
        records = json.loads(request.POST.get("records")) # records ids that need links
        email = json.loads(request.POST.get("email")) # flag to send links by email or not
        cached_records = cache.get("form_records_request") # state of request to check if records ids are the same and to limit email mailing
        if email and cached_records is None:
            cache.set(
                "form_records_request",
                {email: True, "expire_time": timezone.now() + timezone.timedelta(seconds=900)},
                timeout=900,
            )
        elif email and cached_records is not None:
            total_seconds = (cached_records["expire_time"] - timezone.now()).total_seconds()
            total_seconds = int(total_seconds)
            message = f"Отправить рассылку сможете после {total_seconds // 60} минут и {total_seconds % 60} секунд"
            return JsonResponse(
                {
                    "form_html": "",
                    "message": message,
                }
            )


        records = Record.objects.all().filter(id__in=records).only("id", "full_name")
        if not records:
            message = "Нету сотрудников для создания ссылок"
            return JsonResponse(
                {
                    "form_html": "",
                    "message": message,
                }
            )

        links = []
        config = RecordFormConfiguration.get_active_config()

        for record in records:
            token = Token.objects.filter(record=record).first()
            if not token:
                token = Token(
                    record=record,
                    phone=config.phone,
                    full_name=config.full_name,
                    email=config.email,
                    image=config.image,
                    position=config.position,
                    department=config.department,
                    room=config.room,
                    attempt_numbers=config.attempts_number,
                    expire_time=timezone.now() + timezone.timedelta(
                        days=config.expire_time_duration
                    )
                )
            elif not token.is_valid():
                token.token = uuid.uuid4()
                token.attempt_numbers = config.attempts_number
                token.expire_time = timezone.now() + timezone.timedelta(
                    days=config.expire_time_duration
                )
                token.is_email_sended = False



            link = request.build_absolute_uri(
                reverse("record_update_form", kwargs={"token": token})
            )

            if email and not token.is_email_sended:
                token.is_email_sended = True
                if settings.DEBUG:
                    print(record.email)
                else:
                    send_mail(
                        "Фото для справочника AUES",
                        f"""
                                                    Здравствуйте, {record.full_name}

                                                    Для справочника сайта AUES нужны ваши недостающие данные, для корректировки ваших данных перейдите по указанной ссылке снизу:
                                                    {link}
                                                    """,
                        "AUES",
                        fail_silently=False,
                        recipient_list=[record.email],
                    )
            links.append({"full_name": record.full_name, "link": link, "is_email_sended": token.is_email_sended, "expire_time": str(token.expire_time.strftime("%Y-%m-%d %H:%M:%S"))})
            token.save()

        if email:
            action = "Отправить рассылку"
        else:
            action = "Получить ссылки"

        LogManager.make_log(
            request=self.request,
            slug="action",
            by_user_id=self.request.user.id,
            next_values={"Ссылки": links},
            action=action,
        )

        if links:
            if email:
                message = "Рассылка сделана"
            else:
                message = "Ссылки для формы созданы"
            return JsonResponse(
                {
                    "form_html": render_to_string(
                        self.template_name,
                        {"links": links},
                        request=request,
                    ),
                    "message": message,
                }
            )
        else:
            message = "Ссылки для формы не созданы"
            return JsonResponse(
                {
                    "form_html": "",
                    "message": message,
                }
            )


class RecordFormConfigurationView(UpdateView):
    model = RecordFormConfiguration
    form_class = RecordFormConfigurationForm
    template_name = "update_form/record_form_configuration.html"

    def get_object(self, queryset=None):
        return RecordFormConfiguration.get_active_config()

    def form_valid(self, form):
        prev_config = self.get_object()
        config = form.save()
        Token.objects.all().update(
            phone=config.phone,
            full_name=config.full_name,
            email=config.email,
            image=config.image,
            position=config.position,
            department=config.department,
            room=config.room,
        )
        LogManager.make_log(
            request=self.request,
            slug="update",
            by_user_id=self.request.user.id,
            prev_values=prev_config,
            next_values=config,
            action="Настроить рассылку",
            model="RecordFormConfiguration",
        )
        return redirect(self.request.path)
