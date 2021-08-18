from django.contrib.auth import login, logout
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User
from .serializers import LoginSerializer, RegisterSerializer


class LoginAPIView(generics.GenericAPIView):
    permission_classess = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({'detail': ['ログインに成功しました']})


class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'detail': ['ログアウトに成功しました']})


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        kwargs.update({'request': self.request})
        return serializer_class(*args, **kwargs)
