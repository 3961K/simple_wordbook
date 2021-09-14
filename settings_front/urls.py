from django.urls import path

from .views import UserInfoUpdateView, UserPasswordChangeView, UserCardsView, \
    UserCardView

app_name = 'settings_front'

urlpatterns = [
    path('user-info/', UserInfoUpdateView.as_view(), name='user_info'),
    path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('cards/', UserCardsView.as_view(), name='cards'),
    path('cards/<uuid:id>/', UserCardView.as_view(), name='card'),
]
