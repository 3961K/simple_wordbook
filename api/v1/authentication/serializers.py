from django.contrib.auth import login, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.fields import empty

from .models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username,
                                password=password)

            # root権限を持つユーザ,staff権限を持つユーザ,アクティブでないユーザはログイン
            # 出来ない様にする
            if user is None or user.is_staff or user.is_superuser or not user.is_active:
                raise serializers.ValidationError('ログインが失敗しました')

            data['user'] = user

        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     style={'input_type': 'password'},
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True,
                                      required=True,
                                      style={'input_type': 'password'},
                                      validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'email': {
                'write_only': True
            },
        }

    def __init__(self, instance=None, data=empty, **kwargs):
        self.instance = instance
        if data is not empty:
            self.initial_data = data
        self.partial = kwargs.pop('partial', False)
        self._context = kwargs.pop('context', {})
        self.request = kwargs.pop('request', None)
        kwargs.pop('many', None)
        super().__init__(**kwargs)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': ['入力されたパスワードが一致しません。']}
            )
        return attrs

    def create(self, validated_data, commit=True):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        login(self.request, user)

        return user
