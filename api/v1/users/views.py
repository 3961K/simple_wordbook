from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from rest_framework.mixins import UpdateModelMixin
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .permissions import IsSelfOrReadOnly
from .serializers import UserSerializer, UserPrivateSerializer, PasswordChangeSerializer
from ..cards.serializers import CardSerializer
from ..cards.views import CardListFilter
from ..wordbooks.serializers import WordbookSerializer
from ..wordbooks.views import WordbookListFilter

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


class UserCardListAPIView(ListAPIView):
    lookup_field = 'username'
    queryset = User.objects.all().prefetch_related('cards')
    serializer_class = CardSerializer
    filter_class = CardListFilter

    def get_user(self):
        """
        URLで指定したユーザを取得する

        Notes
        -----
        get_objectはカードを取り扱うため,識別子で指定したユーザを取得するための関数を用意した
        """
        # URLに含まれているユーザ名からユーザを取得する
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        user = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, user)

        return user

    def get_queryset(self):
        """
        URLに含まれているユーザ名からユーザを取得した後に,そのユーザが作成したカード群を
        アクセスしてきたユーザに応じてquerysetとして返す様にオーバーライドしたget_queryset

        Notes
        -----
        ユーザ自身がアクセスしてきた場合は非公開カードも返し,ユーザ自身でない場合は公開カード
        のみが返される
        """
        # URLで指定したユーザを取得
        user = self.get_user()

        # アクセスしてきたユーザに応じて返すカードを変更している
        queryset = user.cards.filter(is_hidden=False).all()
        if user.id == self.request.user.id:
            queryset = user.cards.all()

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        return queryset


class UserWordbookListAPIView(ListAPIView):
    lookup_field = 'username'
    queryset = User.objects.all().prefetch_related('wordbooks')
    serializer_class = WordbookSerializer
    filter_class = WordbookListFilter

    def get_user(self):
        """
        URLで指定したユーザを取得する

        Notes
        -----
        get_objectは単語帳を取り扱うため,識別子で指定したユーザを取得するための関数を用意した
        """
        # URLに含まれているユーザ名からユーザを取得する
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        user = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, user)

        return user

    def get_queryset(self):
        """
        URLに含まれているユーザ名からユーザを取得した後に,そのユーザが作成した単語帳群を
        アクセスしてきたユーザに応じてquerysetとして返す様にオーバーライドしたget_queryset

        Notes
        -----
        ユーザ自身がアクセスしてきた場合は非公開単語帳も返し,ユーザ自身でない場合は公開単語帳
        のみが返される
        """
        # URLで指定したユーザを取得
        user = self.get_user()

        # アクセスしてきたユーザに応じて返す単語帳を変更している
        queryset = user.wordbooks.filter(is_hidden=False).all()
        if user.id == self.request.user.id:
            queryset = user.wordbooks.all()

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        return queryset


class OnlyPartialAPIView(UpdateModelMixin, GenericAPIView):
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class PasswordChangeAPIView(OnlyPartialAPIView):
    lookup_field = 'username'
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        kwargs.update({'user': self.request.user})
        return serializer_class(*args, **kwargs)
