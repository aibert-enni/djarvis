# Generated by Django 5.1.4 on 2024-12-13 10:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipphone_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='is_email_sended',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='token',
            name='expire_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
