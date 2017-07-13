from django.conf.urls import url
from  .import views

app_name = "shadowsocks"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^nodeinfo$',views.nodeinfo,name='nodeinfo'),
]
