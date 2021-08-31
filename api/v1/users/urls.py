from django.urls import path

from .views import UserListAPIView, UserRetrieveUpdateDestroyAPIView,\
    UserCardListAPIView, UserWordbookListAPIView, PasswordChangeAPIView

app_name = 'users'

urlpatterns = [
    path('', UserListAPIView.as_view(), name='list'),
    path('<str:username>/', UserRetrieveUpdateDestroyAPIView.as_view(),
         name='detail'),
    path('<str:username>/cards/', UserCardListAPIView.as_view(),
         name='cards'),
    path('<str:username>/wordbooks/', UserWordbookListAPIView.as_view(),
         name='wordbooks'),
    path('<str:username>/change-password/', PasswordChangeAPIView.as_view(),
         name='change_password'),
]
