from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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
