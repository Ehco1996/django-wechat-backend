from rest_framework.validators import UniqueValidator

from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.trade.models import MoneyCode


class MoneyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyCode
        fields = '__all__'


class ChagreSerializer(serializers.Serializer):
    '''
    充值请求序列话
    '''
    user_id = serializers.IntegerField(help_text='用户id')
    code = serializers.CharField(help_text='充值码')

    class Meta:
        fields = ('user_id', 'code')

    def validated_code(self, code):
        '''
        验证充值码
        '''
        if not MoneyCode.objects.filter(code=code, isused=False).exists():
            raise serializers.ValidationError('充值码不正确')
        else:
            return code
