from django.contrib import admin
from .models import Record, Department, RecordFormConfiguration, Token

admin.site.register(Department)
admin.site.register(Record)
admin.site.register(RecordFormConfiguration)
admin.site.register(Token)