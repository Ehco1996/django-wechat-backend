from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth import get_user_model

from .models import InviteCode
from .permissions import IsOwnerOrReadOnly

# 获取当前用户模型
User = get_user_model()

from .serializers import UserSerializer, InviteCodeSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class InviteCodeList(generics.ListCreateAPIView):
    queryset = InviteCode.objects.all()
    serializer_class = InviteCodeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class InviteCodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = InviteCode.objects.all()
    serializer_class = InviteCodeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
