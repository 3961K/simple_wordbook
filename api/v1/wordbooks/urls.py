from django.urls import path

from .views import WordbookListCreateAPIView

app_name = 'wordbooks'

urlpatterns = [
    path('', WordbookListCreateAPIView.as_view(), name='list'),
]
