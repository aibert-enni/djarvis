# Generated by Django 5.1.4 on 2024-12-20 16:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipphone_app', '0002_token_is_email_sended_alter_token_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.RegexValidator(code='invalid_email', message='Почта должна быть в формате username@aues.kz.', regex='^[a-zA-Z0-9._%+-]+@aues\\.kz$')]),
        ),
        migrations.AlterField(
            model_name='record',
            name='full_name',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(code='invalid_full_name', message='ФИО должна начинаться с заглавной буквы и содержать только буквы', regex='^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+(?: [А-ЯЁ][а-яё]+)?$')]),
        ),
        migrations.AlterField(
            model_name='record',
            name='phone',
            field=models.IntegerField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='room',
            field=models.CharField(blank=True, max_length=5, null=True, validators=[django.core.validators.RegexValidator(code='invalid_room', message='Номер кабинета должна быть в формате А-2341', regex='^[А-Я]-\\d{3}$')]),
        ),
    ]
