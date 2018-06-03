from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from . import models


def delete_with_file(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete()


class UserPicAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'image', 'display_photo', 'create_at']
    search_fields = ['user_id', 'create_at']
    readonly_fields = ['display_photo', ]
    actions = [delete_with_file]

    def display_photo(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url,
            width=obj.image.width,
            height=obj.image.height,
        ))

    display_photo.allow_tags = True


class ReplyRuleAdmin(admin.ModelAdmin):
    list_display = ['key_word', 'content', 'create_at']
    search_fields = ['key_word', ]


admin.site.register(models.UserPic, UserPicAdmin)
admin.site.register(models.ReplyRule, ReplyRuleAdmin)


admin.site.unregister(Group)
