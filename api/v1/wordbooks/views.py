from django.db.models.query import QuerySet
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView, ListCreateAPIView, ListAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Wordbook
from .serializers import WordbookSerializer, WordbookRetrieveSerializer, \
    WordbookCreateSerializer, WordbookUpdateSerializer
from ..cards.serializers import CardSerializer
from .permissions import IsNotAuthorReadPublicOnly, IsAuthorReadOnly


class WordbookListFilter(filters.FilterSet):
    q = filters.CharFilter(field_name='wordbook_name', lookup_expr='contains')

    class Meta:
        model = Wordbook
        fields = ['wordbook_name']


class WordbookListCreateAPIView(ListCreateAPIView):
    queryset = Wordbook.objects.filter(is_hidden=False).all()
    serializer_class = WordbookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_class = WordbookListFilter

    def get_serializer_class(self):
        http_method = self.request.method
        if self.request.user.is_authenticated and http_method == 'POST':
            return WordbookCreateSerializer
        return self.serializer_class


class RetrieveDeletePartialUpdateAPIView(RetrieveModelMixin,
                                         UpdateModelMixin,
                                         DestroyModelMixin,
                                         GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class WordbookRetrieveDeletePartialUpdateAPIView(RetrieveDeletePartialUpdateAPIView):
    queryset = Wordbook.objects.all()
    serializer_class = WordbookRetrieveSerializer
    permission_classes = [IsNotAuthorReadPublicOnly]
    lookup_field = 'id'

    def get_serializer_class(self):
        http_method = self.request.method
        if http_method == 'PATCH':
            return WordbookUpdateSerializer
        return self.serializer_class

    def get_permissions(self):
        # パーミッションクラスにアクセスしたURLに含まれる単語帳を渡す
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        wordbook_id = self.kwargs[lookup_url_kwarg]
        wordbook = get_object_or_404(Wordbook, id=wordbook_id)
        return [permission(wordbook=(wordbook))
                for permission in self.permission_classes]


class WordbookCardListAPIView(ListAPIView):
    queryset = Wordbook.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthorReadOnly]
    lookup_field = 'id'

    def get_wordbook(self):
        """
        URLで指定した単語帳を取得する

        Notes
        -----
        get_objectはカードを取り扱うため,識別子で指定した単語帳を取得するための関数を用意した
        """
        # URLに含まれているIDから単語帳を取得する
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
        wordbook = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, wordbook)

        return wordbook

    def get_queryset(self):
        """
        URLに含まれているIDから単語帳を取得した後に,その単語帳に含まれているカード群を
        アクセスしてきたユーザに応じてquerysetとして返す様にオーバーライドしたget_queryset

        Notes
        -----
        単語帳の作者の場合は単語帳に含まれる非公開カードも返し,作者でない場合は単語帳に
        含まれる公開カードのみが返される
        """
        # URLで指定した単語帳を取得
        wordbook = self.get_wordbook()

        # 単語帳に格納されているカード群からアクセスしてきたユーザに応じて,返すカード群を変更
        queryset = wordbook.cards.filter(is_hidden=False).all()
        if wordbook.author.id == self.request.user.id:
            queryset = wordbook.cards.all()

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        return queryset
