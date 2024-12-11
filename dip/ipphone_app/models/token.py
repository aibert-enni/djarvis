import uuid

from django.conf import settings
from django.db import models
from django.utils.timezone import now

from ipphone_app.models.record import Record


def default_edit_fields_permissions():
    return settings.EDIT_FIELDS_PERMISSIONS

class Token(models.Model):
    token = models.UUIDField(default=uuid.uuid4)
    record = models.OneToOneField(Record, on_delete=models.CASCADE)
    attempt_numbers = models.IntegerField(default=0)
    expire_time = models.DateTimeField(default=now)

    # permissions for record update
    phone = models.BooleanField(default=False)
    full_name = models.BooleanField(default=False)
    department = models.BooleanField(default=False)
    position = models.BooleanField(default=False)
    room = models.BooleanField(default=False)
    email = models.BooleanField(default=False)
    image = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.token}"