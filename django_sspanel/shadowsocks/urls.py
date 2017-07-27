from django.conf.urls import url
from  .import views



app_name = "shadowsocks"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^nodeinfo/$',views.nodeinfo,name='nodeinfo'),
    url(r'^sshelp/$',views.sshelp,name='sshelp'),
    url(r'^ssclient/$',views.ssclient,name='ssclient'),
    url(r'^ssinvite/$',views.ssinvite,name='ssinvite'),
    url(r'^ssinvite_gen_code/(?P<Num>[0-9]{1,2})/$',views.gen_invite_code,name='geninvitecode'),# 前期调试使用，后期会加入权限
    url(r'^passinvite/(?P<invitecode>[\S]+)/$',views.pass_invitecode,name='passinvitecode'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$',views.Login_view,name='login'),
    url(r'^logout/$',views.Logout_view,name='logout'),
    url(r'^users/userinfo/$',views.userinfo,name='userinfo'),
    url(r'^users/userinfo_edit/$',views.userinfo_edit,name='userinfo_edit'),
    url(r'^checkin/$',views.checkin,name='checkin'),
    url(r'qrcode/(?P<node_id>[0-9]+)$',views.get_ss_qrcode,name='qrcode'),
    ]
