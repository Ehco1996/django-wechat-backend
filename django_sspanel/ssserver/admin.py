from django.contrib import admin
from . import models


class InviteCode(admin.ModelAdmin):
    list_display=['code','time_created']


# Register your models here.
admin.site.register(models.Node)
admin.site.register(models.InviteCode,InviteCode)


