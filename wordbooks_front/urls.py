from django.urls import path

from .views import WordbooksView, WordbookView, WordbookCreateView

app_name = 'wordbooks_front'

urlpatterns = [
    path('', WordbooksView.as_view(), name='list'),
    path('new-wordbook/', WordbookCreateView.as_view(), name='new_wordbook'),
    path('<uuid:id>/', WordbookView.as_view(), name='detail'),
]
