from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db import models

from ipphone_app.models.department import Department


class Record(models.Model):
    # email_validator = RegexValidator(
    #     regex=r'^[a-zA-Z0-9._%+-]+@aues\.kz$',
    #     message='Почта должна быть в формате username@aues.kz.',
    #     code='invalid_email'
    # )

    # room_validator = RegexValidator(
    #     regex=r'^[А-Я]-\d{3}$',
    #     message='Номер кабинета должна быть в формате А-234',
    #     code='invalid_room'
    # )

    # full_name_validator = RegexValidator(
    #     regex=r'^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+(?: [А-ЯЁ][а-яё]+)?$',
    #     message='ФИО должна начинаться с заглавной буквы и содержать только буквы',
    #     code='invalid_full_name'
    # )

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )

    is_working = models.BooleanField(default=True, verbose_name="Статус занятости")

    phone = models.SmallIntegerField(blank=True, null=True, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    full_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=200, blank=True)
    position_id = models.IntegerField(default=1, blank=True, verbose_name="Позиция")
    room = models.CharField(max_length=5, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="records/", blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}, {self.position}"
