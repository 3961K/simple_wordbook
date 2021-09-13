from django.urls import path

from .views import ForbiddenView, NotFoundView

app_name = 'error_front'

urlpatterns = [
    path('403/', ForbiddenView.as_view(), name='403'),
    path('404/', NotFoundView.as_view(), name='404'),
]
