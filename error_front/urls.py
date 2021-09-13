from django.urls import path

from .views import ForbiddenView

app_name = 'error_front'

urlpatterns = [
    path('403/', ForbiddenView.as_view(), name='403'),
]
