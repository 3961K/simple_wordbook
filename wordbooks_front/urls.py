from django.urls import path

from .views import WordbooksView, WordbookView

app_name = 'wordbooks_front'

urlpatterns = [
    path('', WordbooksView.as_view(), name='list'),
    path('<uuid:id>/', WordbookView.as_view(), name='detail'),
]
