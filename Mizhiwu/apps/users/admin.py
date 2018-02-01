from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'port',
                    'balance', 'level', 'level_expire_time', ]
    search_fields = ['username', 'email', 'id']


class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'owner', 'time_created', 'isused', ]
    search_fields = ['code', 'code_owner', ]


admin.site.register(models.User, UserAdmin)
admin.site.register(models.InviteCode, InviteCodeAdmin)
