from django.contrib import admin
from .models import User,Node,InviteCode,Aliveip


class UserAdmin(admin.ModelAdmin):
        list_display=['username','balance',]
 
class InviteCodeAdmin(admin.ModelAdmin):
    list_display=['code','time_created']

class AliveipAdmin(admin.ModelAdmin):
    list_display=['user_name','ip_address','time']
# Register your models here.
admin.site.register(User,UserAdmin)
admin.site.register(InviteCode,InviteCodeAdmin)
admin.site.register(Node)
admin.site.register(Aliveip,AliveipAdmin)
