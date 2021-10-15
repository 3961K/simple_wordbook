from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.fields import empty

from .models import Wordbook
from ..cards.models import Card

User = get_user_model()


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


class WordbookRetrieveSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField('get_author_name')

    class Meta:
        model = Wordbook
        fields = ['id', 'wordbook_name', 'create_date', 'is_hidden',
                  'author_name']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'wordbook_name': {
                'read_only': True
            },
            'create_date': {
                'read_only': True
            },
            'is_hidden': {
                'read_only': True
            },
            'author_name': {
                'read_only': True
            },
        }

    def get_author_name(self, wordbook):
        author_id = wordbook.author.id
        author = User.objects.get(id=author_id)
        return author.username


class WordbookUpdateSerializer(serializers.Serializer):
    wordbook_name = serializers.CharField(max_length=100, write_only=True)
    is_hidden = serializers.BooleanField(write_only=True)
    add_cards = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )
    delete_cards = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )

    def __init__(self, instance=None, data=empty, **kwargs):
        self.user = kwargs.pop('user', AnonymousUser)
        super().__init__(instance, data, **kwargs)

    def add_cards_to_wordbook(self, instance, add_card_id_list):
        # 逆参照を利用して単語帳にカードを追加
        add_cards = Card.objects.filter(id__in=add_card_id_list).all()
        if len(add_cards) != 0:
            for card in add_cards:
                # 単語帳に非公開であるのに異なるユーザが作成したカードが含まれていた場合は,
                # そのカードを単語帳に追加しない様にする
                if card.is_hidden and card.author != self.user:
                    continue
                instance.cards.add(card)
                instance.save()

    def delete_cards_from_wordbook(self, instance, delete_card_id_list):
        # 逆参照を利用して単語帳からカードを削除
        delete_cards = Card.objects.filter(id__in=delete_card_id_list).all()
        if len(delete_cards) != 0:
            for card in delete_cards:
                instance.cards.remove(card)
                instance.save()

    def update(self, instance, validated_data):
        # 各項目の値の更新を行う
        for key in validated_data.keys():
            if key == 'add_cards':
                self.add_cards_to_wordbook(instance, validated_data['add_cards'])
                continue
            elif key == 'delete_cards':
                self.delete_cards_from_wordbook(instance, validated_data['delete_cards'])
                continue
            else:
                setattr(instance, key, validated_data[key])

        # 変更を反映してからインスタンスを返す
        instance.save()
        return instance


class WordbookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wordbook
        fields = ['wordbook_name', 'is_hidden', 'id', 'create_date']
        extra_kwargs = {
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
