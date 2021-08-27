from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail, ValidationError
from .models import Wordbook


class WordbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wordbook
        fields = ['id', 'wordbook_name']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'wordbook_name': {
                'read_only': True
            }
        }


class WordbookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wordbook
        fields = ['wordbook_name', 'is_hidden', 'id', 'create_date']
        extra_kwargs = {
            'is_hidden': {
                'write_only': True
            },
            'id': {
                'read_only': True
            },
            'create_date': {
                'read_only': True
            },
        }

    def is_valid(self, raise_exception=False):
        result = super().is_valid(raise_exception)

        # authorをHTTPリクエストを送信してきたユーザに指定する
        if not hasattr(self.context['request'], 'user'):
            self._errors = {'author': [
                ErrorDetail(string='ユーザ認証ユーザではありません。')
            ]}
            if raise_exception:
                raise ValidationError(self._errors)
        else:
            user = self.context['request'].user
            self._validated_data['author'] = user

        return result and not bool(self._errors)
