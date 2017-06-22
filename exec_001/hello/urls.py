from django.conf.urls import url
from .import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'hello'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about', views.about, name='about'),
    url(r'category/(?P<category_name>\w+)/$',views.category,name='category')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
