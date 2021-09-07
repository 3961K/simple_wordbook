from django.urls import path

from .views import CardsView, CardView, CardCreateView

app_name = 'cards_front'

urlpatterns = [
    path('', CardsView.as_view(), name='list'),
    path('new-card/', CardCreateView.as_view(), name='new_card'),
    path('<uuid:id>/', CardView.as_view(), name='detail'),
]
