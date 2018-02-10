from django.contrib import admin
from . import models


class MoneyCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'isused', ]
    search_fields = ['user', 'code']


admin.site.register(models.MoneyCode, MoneyCodeAdmin)
