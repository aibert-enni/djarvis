from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    position = models.IntegerField(default=1, blank=True)

    def __str__(self):
        return self.name