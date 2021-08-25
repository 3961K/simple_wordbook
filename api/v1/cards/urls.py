from django.urls import path

from .views import CardListCreateAPIView

app_name = 'cards'

urlpatterns = [
    path('', CardListCreateAPIView.as_view(), name='list'),
]
