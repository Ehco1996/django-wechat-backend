
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import InviteCode

# 获取当前用户模型
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'invite_user')
        # fields = '__all__'


class InviteCodeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = InviteCode
        fields = '__all__'
