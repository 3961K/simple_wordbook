from django.urls import path, include

app_name = 'v1'

urlpatterns = [
    path('authentication/', include('api.v1.authentication.urls')),
    path('users/', include('api.v1.users.urls')),
    path('cards/', include('api.v1.cards.urls')),
    path('wordbooks/', include('api.v1.wordbooks.urls')),
]
