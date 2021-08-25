from django_filters import rest_framework as filters
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Card
from .serializers import CardSerializer, CardCreateSerializer


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
