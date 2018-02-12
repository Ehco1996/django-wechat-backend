from django.contrib import admin
from . import models


class MoneyCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'isused', ]
    search_fields = ['user', 'code']


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['info', 'number', 'level', ]


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['info', 'user', 'number', 'create_time']
    search_fields = ['user', ]


admin.site.register(models.MoneyCode, MoneyCodeAdmin)
admin.site.register(models.Goods, GoodsAdmin)
admin.site.register(models.PurchaseHistory, PurchaseAdmin)
