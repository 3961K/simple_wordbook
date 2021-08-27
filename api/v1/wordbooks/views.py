from django_filters import rest_framework as filters
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Wordbook
from .serializers import WordbookSerializer, WordbookCreateSerializer


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
