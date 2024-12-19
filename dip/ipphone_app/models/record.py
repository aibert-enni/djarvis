from django.core.validators import RegexValidator
from django.db import models

from ipphone_app.models.department import Department


class Record(models.Model):
    email_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9._%+-]+@aues\.kz$',
        message='Почта должна быть в формате username@aues.kz.',
        code='invalid_email'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    full_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=200, blank=True)
    position_id = models.IntegerField(default=1, blank=True, verbose_name="Позиция")
    room = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True, validators=[email_validator])
    image = models.ImageField(upload_to="records/", blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}, {self.position}"
