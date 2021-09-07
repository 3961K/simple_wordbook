from django.urls import path

from .views import CardsView, CardCreateView

app_name = 'cards_front'

urlpatterns = [
    path('', CardsView.as_view(), name='list'),
    path('new-card/', CardCreateView.as_view(), name='new_card'),
]
