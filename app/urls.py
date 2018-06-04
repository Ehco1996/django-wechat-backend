from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path

urlpatterns = [
    re_path(r'^jet/', include('jet.urls', 'jet')),
    path('', admin.site.urls),
    path('api/wechat/', include('app.wechat.urls')),
]

if settings.DEBUG is True:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
