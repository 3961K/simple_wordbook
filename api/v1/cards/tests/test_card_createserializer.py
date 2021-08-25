from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from ..models import Card
from ..serializers import CardCreateSerializer

User = get_user_model()


class CardCreateSerializerTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(
            username='card_serializer',
            email='card_serializer@test.com',
            password='testpassw0rd123',
        )

    def test_1_valid_and_success_create(self):
        # 適切な入力値は妥当であり,カードを作成する事が出来る
        user = User.objects.get(username='card_serializer')
        params = {
            'word': 'valid_and_success_create',
            'answer': 'valid_and_success_create',
            'is_hidden': True,
        }
        # バリデーション結果を検証
        request = APIRequestFactory().post(reverse('api:v1:cards:list'))
        request.user = user
        serializer = CardCreateSerializer(data=params, context={'request': request})
        self.assertTrue(serializer.is_valid())
        # カードが作成される事を確認
        serializer.save()
        card = Card.objects.get(word='valid_and_success_create')
        self.assertIsNotNone(card)

    def test_2_invalid_unauthorizationed(self):
        # 認証されていない場合は適当な入力値であっても妥当ではない
        params = {
            'word': 'valid_and_success_create',
            'answer': 'valid_and_success_create',
            'is_hidden': True,
        }
        request = APIRequestFactory().post(reverse('api:v1:cards:list'))
        # バリデーション結果を検証
        serializer = CardCreateSerializer(data=params, context={'request': request})
        self.assertFalse(serializer.is_valid())

    def test_3_invalid_wrong_params(self):
        # 不適切な入力値は妥当ではない
        user = User.objects.get(username='card_serializer')
        wrong_params_list = [
            {
                'word': 'A' * 101,
                'answer': 'valid_and_success_create',
                'is_hidden': True,
            },
            {
                'word': 'valid_and_success_create',
                'answer': 'A' * 201,
                'is_hidden': True,
            },
            {
                'word': 'valid_and_success_create',
                'answer': 'A' * 201,
                'is_hidden': True,
            },
        ]

        # バリデーション結果を検証
        request = APIRequestFactory().post(reverse('api:v1:cards:list'))
        request.user = user
        for wrong_params in wrong_params_list:
            serializer = CardCreateSerializer(data=wrong_params,
                                              context={'request': request})
            self.assertFalse(serializer.is_valid(raise_exception=False))
