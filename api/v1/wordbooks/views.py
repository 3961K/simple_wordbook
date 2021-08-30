from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin

from .models import Wordbook
from .serializers import WordbookSerializer, WordbookRetrieveSerializer, \
    WordbookCreateSerializer, WordbookUpdateSerializer
from .permissions import IsNotAuthorReadPublicOnly


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
