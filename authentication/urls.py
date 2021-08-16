from django.urls import path

from .views import LoginAPIView

app_name = 'authentication'

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
]
