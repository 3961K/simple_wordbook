from django.urls import path

from .views import UserinfoUpdateView

app_name = 'settings_front'

urlpatterns = [
    path('user-info/', UserinfoUpdateView.as_view(), name='user_info'),
]
