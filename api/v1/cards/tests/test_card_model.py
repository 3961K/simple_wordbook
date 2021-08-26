from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APITestCase

from ..models import Card
from ...wordbooks.models import Wordbook

User = get_user_model()


class CardTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User(username='card_model',
                    email='card_model@test.com',
                    password='testpassw0rd123')
        user.save()

        Wordbook.objects.create(
            wordbook_name='card_test',
            is_hidden=False,
            author=user
        )

        Wordbook.objects.create(
            wordbook_name='card_test2',
            is_hidden=False,
            author=user
        )

    def test_1_success_create_and_delete(self):
        # カードを作成し,削除する事が出来る
        user = User.objects.get(username='card_model')

        Card.objects.create(
            word='create_and_delete',
            answer='create_and_delete',
            author=user,
        )

        # 作成できるか確認
        card = Card.objects.get(word='create_and_delete')
        self.assertIsNotNone(card)
        # 削除できるか確認
        card.delete()
        with self.assertRaises(ObjectDoesNotExist):
            card = Card.objects.get(word='create_and_delete')

    def test_2_success_delete_by_deleting_author(self):
        # カードのauthorを削除する事で自動的にカードが削除される
        user = User.objects.get(username='card_model')

        Card.objects.create(
            word='delete_by_deleting_author',
            answer='delete_by_deleting_author',
            author=user,
        )
        card = Card.objects.get(word='delete_by_deleting_author')
        self.assertIsNotNone(card)

        # authorの削除によってカードの削除ができるか確認
        user.delete()
        with self.assertRaises(ObjectDoesNotExist):
            card = Card.objects.get(word='delete_by_deleting_author')

    def test_3_get_wordbooks_by_reference(self):
        # 参照によってそのカードが属する単語帳を取得する事が出来る
        user = User.objects.get(username='card_model')
        wordbook = Wordbook.objects.get(wordbook_name='card_test')
        wordbook2 = Wordbook.objects.get(wordbook_name='card_test2')

        card = Card(
            word='get_wordbooks_by_reference',
            answer='get_wordbooks_by_reference',
            author=user,
        )
        card.wordbooks.add(wordbook)
        card.wordbooks.add(wordbook2)
        card.save()

        card2 = Card(
            word='get_wordbooks_by_reference2',
            answer='get_wordbooks_by_reference2',
            author=user,
        )
        card2.wordbooks.add(wordbook)
        card2.save()

        # 単語帳に登録されたか確認
        self.assertEqual(len(card.wordbooks.all()), 2)
        self.assertEqual(len(card2.wordbooks.all()), 1)
