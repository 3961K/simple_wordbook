from django.urls import path

from .views import LoginView

app_name = 'authentication_front'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]
