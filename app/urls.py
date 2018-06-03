from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('', admin.site.urls),
    path('wechat/', include('app.wechat.urls')),
]

if settings.DEBUG is True:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
