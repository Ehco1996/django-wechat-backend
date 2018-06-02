from django.urls import path

from . import views


app_name = 'wecaht'
urlpatterns = [
    path('', views.wechat, name='wechat'),
]
