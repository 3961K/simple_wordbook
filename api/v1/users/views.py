from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from .permissions import IsSelfOrReadOnly
from .serializers import UserSerializer, UserPrivateSerializer

User = get_user_model()


class UserListFilter(filters.FilterSet):
    q = filters.CharFilter(field_name='username', lookup_expr='contains')

    class Meta:
        model = User
        fields = ['username']


class UserListAPIView(ListAPIView):
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    filter_class = UserListFilter


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    指定したユーザの詳細情報の取得,情報の更新,削除を行うAPIView
    """
    lookup_field = 'username'
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsSelfOrReadOnly]

    def get_serializer_class(self):
        # アクセスしてきたユーザのユーザ名と情報を取得するユーザ名が一致する場合はシリアライザを切り替える
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        username_in_url = self.kwargs[lookup_url_kwarg]

        if self.request.user.username == username_in_url:
            return UserPrivateSerializer
        return self.serializer_class

    def get_permissions(self):
        # パーミッションクラスにアクセスしたURLに含まれるユーザ名を渡す
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        return [permission(username=(self.kwargs[lookup_url_kwarg]))
                for permission in self.permission_classes]
