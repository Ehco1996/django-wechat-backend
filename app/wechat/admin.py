from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from . import models


def delete_with_file(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete()


class UserPicAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'image', 'thumbnail', 'create_at']
    search_fields = ['user_id', 'create_at']
    list_filter = ['user_id', 'create_at']
    readonly_fields = ['thumbnail', ]
    actions = [delete_with_file]

    list_per_page = 10

    def thumbnail(self, obj):
        if obj.image.width > obj.image.height:
            width = 350
            height = 200
        else:
            width = 200
            height = 350

        return mark_safe('<img src="{}" width="{}" height={} />'.format(
            obj.image.url, width, height,))

    thumbnail.allow_tags = True
    thumbnail.short_description = '缩略图'
    # create.short_description = '缩略图'


class ReplyRuleAdmin(admin.ModelAdmin):
    list_display = ['key_word', 'content', 'create_at']
    search_fields = ['key_word', ]


admin.site.register(models.UserPic, UserPicAdmin)
admin.site.register(models.ReplyRule, ReplyRuleAdmin)


admin.site.unregister(Group)
