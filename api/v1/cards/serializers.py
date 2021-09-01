from django.contrib.auth import get_user_model
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework import serializers

from .models import Card

User = get_user_model()


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'word', 'answer']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'word': {
                'read_only': True
            },
            'answer': {
                'read_only': True
            },
        }


class CardRetrieveSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField('get_author_name')

    class Meta:
        model = Card
        fields = ['word', 'answer', 'is_hidden', 'id', 'create_date', 'author_name']
        extra_kwargs = {
            'word': {
                'read_only': True
            },
            'answer': {
                'read_only': True
            },
            'is_hidden': {
                'read_only': True
            },
            'id': {
                'read_only': True
            },
            'create_date': {
                'read_only': True
            },
            'author_name': {
                'read_only': True
            }
        }

    def get_author_name(self, card):
        author_id = card.author.id
        author = User.objects.get(id=author_id)
        return author.username


class CardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['word', 'answer', 'is_hidden', 'id', 'create_date']

        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'create_date': {
                'read_only': True
            }
        }


class CardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['word', 'answer', 'is_hidden', 'id', 'create_date']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'create_date': {
                'read_only': True
            }
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
