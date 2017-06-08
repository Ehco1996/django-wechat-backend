from django.conf.urls import url
from . import views

app_name = 'imgserver'
urlpatterns = [
    url(r'^$', views.index, name='imgserver'),
    url(r'^img/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$',
        views.placeholder, name='placeholder'),
]
