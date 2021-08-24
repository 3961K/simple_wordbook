from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from ..serializers import RegisterSerializer

User = get_user_model()


class RegisterSerializerTest(APITestCase):

    def test_valid(self):
        # 正しいユーザ情報は登録情報として妥当
        input_data = {
            'username': 'register_serializer',
            'email': 'register_serializer@test.com',
            'password': 'testpassw0rd123',
            'password2': 'testpassw0rd123',
        }

        # バリデーション結果の確認
        serializer = RegisterSerializer(data=input_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid(self):
        # ユーザ情報において誤った形式の入力値が含まれる場合は妥当でない
        input_data_list = [
            {
                'username': 'A' * 31,
                'email': 'register_serializer@test.com',
                'password': 'testpassw0rd123',
                'password2': 'testpassw0rd123',
            },
            {
                'username': 'register_serializer',
                'email': 'a@a.a',
                'password': 'testpassw0rd123',
                'password2': 'testpassw0rd123',
            },
            {
                'username': 'register_serializer',
                'email': 'register_serializer@test.com',
                'password': 'testpassw0rd123',
                'password2': 'testpassw0rd1232',
            },
        ]

        for input_data in input_data_list:
            serializer = RegisterSerializer(data=input_data)
            self.assertFalse(serializer.is_valid())

    def test_invalid2(self):
        # ユーザ情報において欠けたフィールドが含まれる場合は妥当でない
        input_data_list = [
            {
                'email': 'register_serializer@test.com',
                'password': 'testpassw0rd123',
                'password2': 'testpassw0rd123',
            },
            {
                'username': 'register_serializer',
                'password': 'testpassw0rd123',
                'password2': 'testpassw0rd123',
            },
            {
                'username': 'register_serializer',
                'email': 'register_serializer@test.com',
                'password2': 'testpassw0rd123',
            },
            {
                'username': 'register_serializer',
                'email': 'register_serializer@test.com',
                'password': 'testpassw0rd123',
            },
        ]

        for input_data in input_data_list:
            serializer = RegisterSerializer(data=input_data)
            self.assertFalse(serializer.is_valid())
