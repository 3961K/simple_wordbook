from django.urls import path

from .views import UsersView, UserCardsView, UserWordbooksView

app_name = 'users_front'

urlpatterns = [
    path('', UsersView.as_view(), name='list'),
    path('<str:username>/', UserCardsView.as_view(), name='top'),
    path('<str:username>/cards/', UserCardsView.as_view(), name='cards'),
    path('<str:username>/wordbooks/', UserWordbooksView.as_view(), name='wordbooks'),
]
