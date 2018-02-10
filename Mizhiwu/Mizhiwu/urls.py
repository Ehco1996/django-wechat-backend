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
from rest_framework_jwt.views import obtain_jwt_token


from users import views as user_view
from trade import views as trade_view

# router相关
router = routers.DefaultRouter()
router.register(r'users', user_view.UserViewSet, base_name='users')
router.register(r'invitecodes', user_view.InviteCodeViewSet,
                base_name='invitecodes')
router.register(r'moneycodes', trade_view.MoneyCodeViewSet,
                base_name='moneycodes')

schema_view = get_schema_view(title='谜之屋API Schema')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', schema_view),
    path('docs/', include_docs_urls(title="谜之屋api文档")),

    # session 认证
    path('api-auth/', include('rest_framework.urls')),
    # jwt token 认证
    re_path(r'^api-token-auth/', obtain_jwt_token),
    # api路由
    re_path(r'^api/', include(router.urls)),
]
