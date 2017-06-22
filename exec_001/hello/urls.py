from django.conf.urls import url
from .import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'hello'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about', views.about, name='about'),
    url(r'^category/(?P<category_name>\w+)/$',views.category,name='category'),
    url(r'^add_category/$',views.add_category,name='add_category'),
    url(r'^add_page/(?P<category_name>\w+)/$',views.add_page,name='add_page'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
