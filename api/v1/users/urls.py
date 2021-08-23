from django.urls import path

from .views import UserListAPIView, UserRetrieveUpdateDestroyAPIView

app_name = 'users'

urlpatterns = [
    path('', UserListAPIView.as_view(), name='list'),
    path('<str:username>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='detail'),
]
