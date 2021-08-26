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

    class Meta:
        model = Card
        fields = ['word']


class CardListCreateAPIView(ListCreateAPIView):
    queryset = Card.objects.filter(is_hidden=False).all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_class = CardListFilter

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
