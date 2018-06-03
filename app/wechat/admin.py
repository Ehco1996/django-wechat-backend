from django.contrib import admin
from django.contrib.auth.models import Group

from . import models


def delete_with_file(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete()


class UserPicAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'image', 'media_id', 'create_at']
    search_fields = ['user_id', 'create_at']
    actions = [delete_with_file]


class ReplyRuleAdmin(admin.ModelAdmin):
    list_display = ['key_word', 'content', 'create_at']
    search_fields = ['key_word', ]


admin.site.register(models.UserPic, UserPicAdmin)
admin.site.register(models.ReplyRule, ReplyRuleAdmin)


admin.site.unregister(Group)
