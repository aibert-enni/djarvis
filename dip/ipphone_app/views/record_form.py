import copy
import uuid
from datetime import timedelta

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
        config = RecordFormConfiguration.objects.get(id=1)
        if not config.is_active:
            return HttpResponseForbidden("Ссылка на данный момент не работает")
        token = kwargs.get("token")
        token = check_token(token)
        if not token:
            return HttpResponseForbidden(
                "Срок действие либо количество попыток истек, попросите заново ссылку"
            )
        token.attempt_numbers += 1
        token.save()
        if token.attempt_numbers > config.attempts_number:
            return HttpResponseForbidden(
                "Срок действие либо количество попыток истек, попросите заново ссылку"
            )
        self.object = token.record
        self.old_object = copy.deepcopy(self.object)
        self.token = token
        return super().dispatch(request, *args, **kwargs)

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
        print(prev_record, record)
        LogManager.make_log(
            slug="update",
            by_user_id=record.id,
            prev_values=prev_record,
            next_values=record,
            model="Record",
        )
        messages.success(self.request, "Ваши данные были обновлены")
        return redirect("home")

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            print(f"Field: {field}, Errors: {errors}")
        return redirect("home")


class SendRecordsFormsView(View):
    template_name = "update_form/record_update_links.html"

    @transaction.atomic
    def post(self, request):
        records = json.loads(request.POST.get("records"))
        email = json.loads(request.POST.get("email"))
        cached_records = cache.get("form_records_request")

        if cached_records is None:
            cache.set(
                "form_records_request",
                {"records": records, "email": email},
                timeout=900,
            )
        elif cached_records["records"] == records:
            if not email or cached_records["email"] == True:
                if email:
                    messages.error(request, "Вы уже делали рассылку")
                else:
                    messages.error(request, "Вы уже запрашивали ссылки")
                form_records_links = cache.get("form_records_links")
                return JsonResponse(
                    {
                        "form_html": render_to_string(
                            self.template_name,
                            {"links": form_records_links},
                            request=request,
                        )
                    }
                )
            elif email:
                cache.set(
                    "form_records_request",
                    {"records": records, "email": email},
                    timeout=900,
                )

        records = Record.objects.all().filter(id__in=records).only("id", "full_name")
        if not records:
            messages.error(request, "Нету сотрудников для создания ссылок")
            return redirect("home")

        links = []
        config = RecordFormConfiguration.objects.only("expire_time_duration").get(id=1)

        for record in records:
            token = Token.objects.filter(record=record).first()
            if not token:
                config = RecordFormConfiguration.objects.get(pk=1)
                token = Token(
                    record=record,
                    phone=config.phone,
                    full_name=config.full_name,
                    email=config.email,
                    image=config.image,
                    position=config.position,
                    department=config.department,
                    room=config.room,
                )
            else:
                token.token = uuid.uuid4()

            token.attempt_numbers = 0
            token.expire_time = timezone.now() + timedelta(
                days=config.expire_time_duration
            )
            token.save()

            link = request.build_absolute_uri(
                reverse("record_update_form", kwargs={"token": token})
            )
            links.append({"full_name": record.full_name, "link": link})

            if email and record.email:
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

        cache.set("form_records_links", links, timeout=900)

        LogManager.make_log(
            request=self.request,
            slug="action",
            by_user_id=self.request.user.id,
            next_values={"Ссылки": links},
            action="Отправить рассылку",
        )

        if links:
            if email:
                messages.success(request, "Рассылка сделана")
            else:
                messages.success(request, "Ссылки для формы созданы")
            return JsonResponse(
                {
                    "form_html": render_to_string(
                        self.template_name,
                        {"links": links},
                        request=request,
                    )
                }
            )
        else:
            messages.error(request, "Ссылки для формы не созданы")
            return redirect("home")


class RecordFormConfigurationView(UpdateView):
    model = RecordFormConfiguration
    form_class = RecordFormConfigurationForm
    template_name = "update_form/record_form_configuration.html"

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
        return redirect(self.request.META.get("HTTP_REFERER"))