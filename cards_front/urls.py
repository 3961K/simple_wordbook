from django.urls import path

from .views import CardsView

app_name = 'cards_front'

urlpatterns = [
    path('', CardsView.as_view(), name='list'),
]
