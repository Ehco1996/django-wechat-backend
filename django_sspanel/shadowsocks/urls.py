from django.conf.urls import url
from  .import views

app_name = "shadowsocks"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^nodeinfo$',views.nodeinfo,name='nodeinfo'),
    url(r'^sshelp$',views.sshelp,name='sshelp'),
    url(r'^ssclient$',views.ssclient,name='ssclient'),
    url(r'^ssinvite$',views.ssinvite,name='ssinvite'),
    url(r'ssinvite/(?P<Num>[0-9]{1,2})/$',views.gen_invite_code,name='geninvitecode'),
    url(r'register/$',views.register,name='register'),
    ]
