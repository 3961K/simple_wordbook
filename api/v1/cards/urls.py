from django.urls import path

from .views import CardListCreateAPIView, CardRetrieveDeletePartialUpdateAPIView

app_name = 'cards'

urlpatterns = [
    path('', CardListCreateAPIView.as_view(), name='list'),
    path('<uuid:id>/', CardRetrieveDeletePartialUpdateAPIView.as_view(),
         name='detail'),
]
