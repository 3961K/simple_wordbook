from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer

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
