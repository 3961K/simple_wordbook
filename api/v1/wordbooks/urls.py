from django.urls import path

from .views import WordbookListCreateAPIView, WordbookRetrieveDeletePartialUpdateAPIView

app_name = 'wordbooks'

urlpatterns = [
    path('', WordbookListCreateAPIView.as_view(), name='list'),
    path('<uuid:id>/', WordbookRetrieveDeletePartialUpdateAPIView.as_view(),
         name='detail'),
]
