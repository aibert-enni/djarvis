from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    position = models.IntegerField(default=1, blank=True)

    def str(self):
        return self.name

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    phone = models.CharField(max_length=15, blank=True,null=True)
    full_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=200, blank=True)
    position_id = models.IntegerField(default=1, blank=True, verbose_name="Позиция")
    room = models.CharField(max_length=150, blank=True,null=True)
    email = models.CharField(max_length=100, blank=True,null=True)

    def str(self):
        return(f"{self.full_name}, {self.position}")
