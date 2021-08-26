from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from ..models import Wordbook
from ..serializers import WordbookCreateSerializer

User = get_user_model()


class WordbooCreatekSerializerTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(
            username='wordbook_create_serializer',
            email='wordbook_create_serializer@test.com',
            password='testpassw0rd123',
        )

    def test_1_valid_and_success_create(self):
        # 適切な入力値は妥当であり,単語帳を作成する事が出来る
        user = User.objects.get(username='wordbook_create_serializer')
        params = {
            'wordbook_name': 'valid_and_success_create',
            'is_hidden': True,
        }
        # バリデーション結果を検証
        request = APIRequestFactory().post(reverse('api:v1:wordbooks:list'))
        request.user = user
        serializer = WordbookCreateSerializer(data=params,
                                              context={'request': request})
        self.assertTrue(serializer.is_valid())
        # 単語帳が作成される事を確認
        serializer.save()
        wordbook = Wordbook.objects.get(wordbook_name='valid_and_success_create')
        self.assertIsNotNone(wordbook)

    def test_2_invalid_unauthorizationed(self):
        # 認証されていない場合は適当な入力値であっても妥当ではない
        params = {
            'wordbook_name': 'valid_and_success_create',
            'is_hidden': True,
        }
        request = APIRequestFactory().post(reverse('api:v1:wordbooks:list'))
        # バリデーション結果を検証
        serializer = WordbookCreateSerializer(data=params,
                                              context={'request': request})
        self.assertFalse(serializer.is_valid())

    def test_3_invalid_unauthorizationed(self):
        # 認証されていない場合は適当な入力値であっても妥当ではない
        wrong_params_list = [
            {
                'wordbook_name': 'A' * 101,
                'is_hidden': True,
            },
            {
                'wordbook_name': 'valid_and_success_create',
                'is_hidden': 'wrong_param',
            }
        ]
        request = APIRequestFactory().post(reverse('api:v1:wordbooks:list'))
        # バリデーション結果を検証
        for wrong_params in wrong_params_list:
            serializer = WordbookCreateSerializer(data=wrong_params,
                                                  context={'request': request})
            self.assertFalse(serializer.is_valid())
