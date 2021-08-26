from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APITestCase

from ..models import Wordbook
from ...cards.models import Card

User = get_user_model()


class WordbookTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User(
            username='wordbook',
            email='wordbook@test.com',
            password='testpassw0rd123'
        )
        user.save()

        for i in range(1, 6):
            Card.objects.create(
                word='wordbook_{}'.format(i),
                answer='wordbook_{}'.format(i),
                author=user,
            )

    def test_1_success_create_and_delete(self):
        # 単語帳を作成し,削除する事が出来る
        user = User.objects.get(username='wordbook')
        Wordbook.objects.create(
            wordbook_name='create_and_delete',
            is_hidden=False,
            author=user
        )

        # 作成できるか確認
        wordbook = Wordbook.objects.get(wordbook_name='create_and_delete')
        self.assertIsNotNone(wordbook)
        # 削除できるか確認
        wordbook.delete()
        with self.assertRaises(ObjectDoesNotExist):
            wordbook = Wordbook.objects.get(wordbook_name='create_and_delete')

    def test_2_success_delete_by_deleting_author(self):
        # カードのauthorを削除する事で自動的に単語帳が削除される
        user = User.objects.get(username='wordbook')
        Wordbook.objects.create(
            wordbook_name='delete_by_deleting_author',
            is_hidden=False,
            author=user
        )

        # 作成されたか確認
        wordbook = Wordbook.objects.get(
            wordbook_name='delete_by_deleting_author')
        self.assertIsNotNone(wordbook)
        # ユーザの削除によって自動的に単語帳が削除される
        user.delete()
        with self.assertRaises(ObjectDoesNotExist):
            wordbook = Wordbook.objects.get(
                wordbook_name='delete_by_deleting_author')

    def test_3_success_get_cards_by_reverse_reference(self):
        # 逆参照によって単語中に追加されているカードの一覧を取得する事が出来る

        # 単語帳の作成
        user = User.objects.get(username='wordbook')
        wordbook = Wordbook(
            wordbook_name='get_cards_by_reverse_reference',
            is_hidden=False,
            author=user
        )
        wordbook.save()
        wordbook = Wordbook.objects.get(
            wordbook_name='get_cards_by_reverse_reference')
        self.assertIsNotNone(wordbook)

        # 各カードのwordbooksに作成したワードブックを追加
        for i in range(1, 6):
            card = Card.objects.get(word='wordbook_{}'.format(i))
            card.wordbooks.add(wordbook)
            card.save()

        # 逆参照によって単語帳に格納されているカードを取得する事が出来る
        # 件数の確認
        self.assertEqual(len(wordbook.cards.all()), 5)
