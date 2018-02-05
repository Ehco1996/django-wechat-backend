from random import randint

from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from .models import InviteCode
from .permissions import IsOwnerOrReadOnly
from .serializers import UserInfoSerializer, UserRegSerializer, InviteCodeSerializer, InviteCodeCreateSerializer

# 获取当前用户模型
User = get_user_model()


class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    提供用户信息的`list`, `create`,`retrive`操作
    """
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    authentication_classes = (
        JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        '''
        根据action 调用不同的serializer
        '''
        if self.action == "retrieve":
            return UserInfoSerializer
        elif self.action == "create":
            return UserRegSerializer
        return UserInfoSerializer

    def get_permissions(self):
        '''
        邀请码权限管理
        '''
        if self.action == 'list':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        '''
        重写创建用户的逻辑
        '''
        # serialize 验证数据
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 创建用户
        user = self.perform_create(serializer)
        # 返回response
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["username"] = user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        '''
        重写数据创建逻辑
        '''
        data = serializer.validated_data
        code = data['code']
        invitecode = InviteCode.objects.get(code=code)
        invitecode.isused = True
        invitecode.save()
        max_port_user = User.objects.order_by('-port').first()
        port = max_port_user.port + randint(1, 3)
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            invite_user=invitecode.owner,
            port=port,
        )
        return user


class InviteCodeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    提供邀请码的 `list`, `create`, `retrieve`操作
    """
    queryset = InviteCode.objects.all()
    serializer_class = InviteCodeSerializer
    authentication_classes = (
        JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        '''
        根据action 调用不同的serializer
        '''
        if self.action == "retrieve":
            return InviteCodeSerializer
        elif self.action == "create":
            return InviteCodeCreateSerializer
        return InviteCodeSerializer

    def get_permissions(self):
        '''
        邀请码权限管理
        '''
        if self.action == 'list':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        '''
        重写创建邀请码逻辑
        '''
        # serialize 验证数据
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 创建用户
        code = self.perform_create(serializer)
        # 返回response
        re_dict = serializer.data
        re_dict["code"] = code.code
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
