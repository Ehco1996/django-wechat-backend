from django.contrib import admin
from .models import User,Node,InviteCode


class UserAdmin(admin.ModelAdmin):
        list_display=['username','balance',]
 
class InviteCodeAdmin(admin.ModelAdmin):
    list_display=['code','time_created']

# Register your models here.
admin.site.register(User,UserAdmin)
admin.site.register(Node)
admin.site.register(InviteCode,InviteCodeAdmin)