

from rest_framework import mixins
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from apps.trade.models import MoneyCode, Goods, PurchaseHistory
from apps.trade.serializers import MoneyCodeSerializer, GoodsSerializer, PurchaseHistorySerializer


class MoneyCodeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    提供充值码的 `list`, `create`, `retrieve` ,`update`操作
    """
    queryset = MoneyCode.objects.all()
    serializer_class = MoneyCodeSerializer
    authentication_classes = (
        JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]


class GoodsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品的 `list`, `create`, `retrieve` ,`update`操作
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    authentication_classes = (
        JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class PurchaseHistoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    购买记录 `list`,`retrieve`操作
    """
    queryset = PurchaseHistory.objects.all()
    serializer_class = PurchaseHistorySerializer
    authentication_classes = (
        JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = [permissions.IsAuthenticated]
