from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'icon']
        extra_kwargs = {
            'username': {
                'read_only': True,
            },
            'icon': {
                'read_only': True,
            },
        }
