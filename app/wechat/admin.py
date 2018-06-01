from django.contrib import admin
from django.contrib.auth.models import Group

from . import models


class UserPicAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'image', 'create_at']
    search_fields = ['user_id', 'create_at']


admin.site.register(models.UserPic, UserPicAdmin)


admin.site.unregister(Group)
