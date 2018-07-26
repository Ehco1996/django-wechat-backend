from django.urls import path

from . import views


app_name = 'wechat'
urlpatterns = [
    path('', views.wechat, name='wechat'),
    path('check-port/', views.check_server_api, name='server_check'),
]
