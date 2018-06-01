from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'wecaht'
urlpatterns = [
    path('', views.wechat, name='wechat'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
