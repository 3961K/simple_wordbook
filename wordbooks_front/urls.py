from django.urls import path

from .views import WordbooksView

app_name = 'wordbooks_front'

urlpatterns = [
    path('', WordbooksView.as_view(), name='list'),
]
