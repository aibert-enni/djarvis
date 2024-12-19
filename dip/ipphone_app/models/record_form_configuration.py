from datetime import timedelta

from django.db import models

class RecordFormConfiguration(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Имя конфигурации')

    # permissions for record update
    is_active = models.BooleanField(default=True)
    phone = models.BooleanField(default=False)
    full_name = models.BooleanField(default=False)
    department = models.BooleanField(default=False)
    position = models.BooleanField(default=False)
    room = models.BooleanField(default=False)
    email = models.BooleanField(default=False)
    image = models.BooleanField(default=False)

    expire_time_duration = models.IntegerField(default=1)
    attempts_number = models.IntegerField(default=100)

    def __str__(self):
        return self.name


    @classmethod
    def get_active_config(cls):
        obj, created = cls.objects.get_or_create(id=1, defaults={"name": "Default config"})
        return obj

