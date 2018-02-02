"""Mizhiwu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls


from users import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='users')
router.register(r'invitecodes', views.InviteCodeViewSet,
                base_name='invitecodes')

schema_view = get_schema_view(title='谜之屋API Schema')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', schema_view),
    path('docs/', include_docs_urls(title="谜之屋api文档")),
    path('api-auth/', include('rest_framework.urls')),
    
    re_path(r'^api/', include(router.urls)),
]
