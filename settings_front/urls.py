from django.urls import path

from .views import DeleteUserView, UserInfoUpdateView, UserPasswordChangeView, UserCardsView, \
    UserCardView, UserWordbooksView, UserAddCardsView, UserDeleteCardsView

app_name = 'settings_front'

urlpatterns = [
    path('user-info/', UserInfoUpdateView.as_view(), name='user_info'),
    path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('cards/', UserCardsView.as_view(), name='cards'),
    path('cards/<uuid:id>/', UserCardView.as_view(), name='card'),
    path('wordbooks/', UserWordbooksView.as_view(), name='wordbooks'),
    path('wordbooks/<uuid:id>/add-cards/', UserAddCardsView.as_view(), name='add_wordbook_cards'),
    path('wordbooks/<uuid:id>/delete-cards/', UserDeleteCardsView.as_view(), name='delete_wordbook_cards'),
    path('delete-user/', DeleteUserView.as_view(), name='delete_user'),
]
