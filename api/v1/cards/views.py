from django.db.models.query import QuerySet
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Card
from .serializers import CardSerializer, CardCreateSerializer, \
    CardRetrieveSerializer, CardUpdateSerializer
from .permissions import IsNotAuthorReadPublicOnly


class CardListFilter(filters.FilterSet):
    q = filters.CharFilter(field_name='word', lookup_expr='contains')
    exclude_wordbook_id = filters.BaseInFilter(field_name='wordbooks',
                                               exclude=True,
                                               lookup_expr='in')

    class Meta:
        model = Card
        fields = ['word', 'wordbooks']


class CardListCreateAPIView(ListCreateAPIView):
    queryset = Card.objects.filter(is_hidden=False).all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_class = CardListFilter

    def get_queryset(self):
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset

        # アクセスしてきたユーザが認証されている場合は作成した非公開カードを追加する
        user = self.request.user
        if user.is_authenticated:
            queryset |= Card.objects.filter(author_id=user.id, is_hidden=True)

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def get_serializer_class(self):
        http_method = self.request.method
        if self.request.user.is_authenticated and http_method == 'POST':
            return CardCreateSerializer
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


class CardRetrieveDeletePartialUpdateAPIView(RetrieveDeletePartialUpdateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardRetrieveSerializer
    permission_classes = [IsNotAuthorReadPublicOnly]
    lookup_field = 'id'

    def get_serializer_class(self):
        http_method = self.request.method
        if http_method == 'PATCH':
            return CardUpdateSerializer
        return self.serializer_class

    def get_permissions(self):
        # パーミッションクラスにアクセスしたURLに含まれるカードを渡す
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        card_id = self.kwargs[lookup_url_kwarg]
        card = get_object_or_404(Card, id=card_id)
        return [permission(card=(card))
                for permission in self.permission_classes]
