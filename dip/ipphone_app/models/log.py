from django.contrib.auth.models import User
from django.db import models


class Log(models.Model):
    by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=500)
    prev_values = models.JSONField(null=True, blank=True)
    next_values = models.JSONField(null=True, blank=True)
    slug = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=24, null=False)
    logged_in_code = models.CharField(max_length=40)

    def __str__(self):
        return f'Действие {self.slug} было сделано пользователем {self.by_user} в {self.created_at}'

    class Meta:
        ordering = ['-created_at']
