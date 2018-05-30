from django.urls import path
from . import views


app_name = 'SS'
urlpatterns = [
    path('', views.wechat, name='wechat'),
    path('pay/test/',views.pay_test,name='pay_test')
]
