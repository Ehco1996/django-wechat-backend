from django.conf.urls import url
from .import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'hello'
urlpatterns = [
    url(r'index', views.index, name='index'),
    url(r'about', views.about, name='about'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
