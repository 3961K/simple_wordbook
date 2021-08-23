from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.fields import empty

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


class UserPrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'icon']

    def validate_icon(self, value):
        if not value:
            raise ValidationError('画像ファイルをアップロードしてください')

        try:
            if value.image.width > 512 or value.image.height > 512:
                raise ValidationError('縦幅・横幅が512pxより大きい画像はアップロードする事が出来ません')
        except AttributeError:
            # ログインユーザの現在のアイコンと異なるファイルにも関わらず画像データが無い場合はエラーとする
            if self.user.icon != value:
                raise ValidationError('画像ファイルをアップロードしてください')

        return value


class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def __init__(self, instance=None, data=empty, **kwargs):
        self.instance = instance
        if data is not empty:
            self.initial_data = data
        self.partial = kwargs.pop('partial', False)
        self._context = kwargs.pop('context', {})
        self.user = kwargs.pop('user', AnonymousUser)
        kwargs.pop('many', None)
        super().__init__(instance=instance, data=data, **kwargs)

    def validate_old_password(self, value):
        if not self.user.check_password(value):
            raise serializers.ValidationError(
                {'old_password': ['入力されたパスワードが間違っています。']}
            )
        return value

    def validate(self, value):
        if value['password'] != value['password2']:
            raise serializers.ValidationError(
                {'password': ['入力されたパスワードが一致しません。']}
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
