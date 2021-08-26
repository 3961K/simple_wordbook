from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from ..models import Card
from ..serializers import CardUpdateSerializer

User = get_user_model()


class CardUpdateSerializerTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create(
            username='card_retrieve_serializer',
            email='card_retrieve_serializer@test.com',
            password='testpassw0rd123',
        )
        user.save()

        Card.objects.create(
            word='card_retrieve_serializer',
            answer='card_retrieve_serializer',
            author=user
        )

    def test_1_valid_and_success_update(self):
        # 適切な入力値は妥当である
        params = {
            'word': 'updated_card_retrieve_serializer',
            'answer': 'updated_card_retrieve_serializer',
            'is_hidden': True,
        }

        card = Card.objects.get(word='card_retrieve_serializer')
        serializer = CardUpdateSerializer(data=params, instance=card)
        # バリデーション結果の検証
        self.assertTrue(serializer.is_valid(raise_exception=True))
        # カード更新の検証
        serializer.save()
        updated_card = Card.objects.get(word='updated_card_retrieve_serializer')
        self.assertIsNotNone(updated_card)
        self.assertEqual(updated_card.answer, 'updated_card_retrieve_serializer')

    def test_2_invalid(self):
        # 不適切な入力値は妥当ではない
        wrong_params_list = [
            {
                'word': '',
                'answer': 'updated_card_retrieve_serializer',
                'is_hidden': True,
            },
            {
                'word': 'updated_card_retrieve_serializer',
                'answer': '',
                'is_hidden': True,
            },
            {
                'word': 'A' * 101,
                'answer': 'updated_card_retrieve_serializer',
                'is_hidden': True,
            },
            {
                'word': 'updated_card_retrieve_serializer',
                'answer': 'A' * 201,
                'is_hidden': True,
            },
            {
                'word': 'updated_card_retrieve_serializer',
                'answer': 'updated_card_retrieve_serializer',
                'is_hidden': 'wrong_param',
            },
        ]

        # バリデーション結果の検証
        for wrong_params in wrong_params_list:
            serializer = CardUpdateSerializer(data=wrong_params)
            self.assertFalse(serializer.is_valid())
