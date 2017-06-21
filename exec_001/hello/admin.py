from django.contrib import admin
from .models import Page,Category

# Register your models here.


class PageAdmin(admin.ModelAdmin):
    list_display=['title','category','url']


admin.site.register(Category)
admin.site.register(Page,PageAdmin)