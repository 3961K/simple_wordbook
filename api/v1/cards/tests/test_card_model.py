from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APITestCase

from ..models import Card

User = get_user_model()


class CardTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(username='create_card',
                                 email='create_card@test.com',
                                 password='testpassw0rd123')

    def test_1_success_create_and_delete(self):
        # カードを作成し,削除する事が出来る
        user = User.objects.get(username='create_card')

        Card.objects.create(
            word="create_card",
            answer="create_card",
            author=user,
        )

        # 作成できるか確認
        card = Card.objects.get(word="create_card")
        self.assertIsNotNone(card)
        # 削除できるか確認
        card.delete()
        with self.assertRaises(ObjectDoesNotExist):
            card = Card.objects.get(word="create_card")

    def test_2_success_delete_by_deleting_author(self):
        # カードのauthorを削除する事で自動的にカードが削除される
        user = User.objects.get(username='create_card')

        Card.objects.create(
            word="create_card",
            answer="create_card",
            author=user,
        )
        # authorの削除によってカードの削除ができるか確認
        user.delete()
        with self.assertRaises(ObjectDoesNotExist):
            card = Card.objects.get(word="create_card")
