from django.urls import path

from .views import UserinfoUpdateView, UserpasswordChangeView

app_name = 'settings_front'

urlpatterns = [
    path('user-info/', UserinfoUpdateView.as_view(), name='user_info'),
    path('password-change/', UserpasswordChangeView.as_view(), name='password_change'),
]
