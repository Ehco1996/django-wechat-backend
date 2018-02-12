from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.conf import settings


from apps.trade.models import MoneyCode, Goods, PurchaseHistory
from users.serializers import UserInfoSerializer


class MoneyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyCode
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = '__all__'


class PurchaseHistorySerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    info = GoodsSerializer()

    class Meta:
        model = PurchaseHistory
        fields = '__all__'
