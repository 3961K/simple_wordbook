from django.contrib.auth import get_user_model
from django.test import TestCase

from ..serializers import LoginSerializer

User = get_user_model()


class LoginSerializerTest(TestCase):
    @classmethod
    def setUpClass(cls):
        User.objects.create_user(username='login_serializer',
                                 email='login_serializer@test.com',
                                 password='testpassw0rd123')
        return super().setUpClass()

    def test_valid(self):
        # 正しいユーザ情報は認証する情報として妥当
        input_data = {
            'username': 'login_serializer',
            'password': 'testpassw0rd123'
        }
        serializer = LoginSerializer(data=input_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid(self):
        # ユーザ名・パスワードが欠けた状態では認証する情報として妥当ではない
        input_data_list = [
            {
                'username': 'invalid_login_serializer',
            },
            {
                'password': 'invalid_testpassw0rd123'
            }
        ]

        for input_data in input_data_list:
            serializer = LoginSerializer(data=input_data)
            self.assertFalse(serializer.is_valid())

    def test_invalid2(self):
        # 誤ったユーザ名・パスワードは認証する情報として妥当ではない
        input_data_list = [
            {
                'username': 'invalid_login_serializer',
                'password': 'testpassw0rd123'
            },
            {
                'username': 'login_serializer',
                'password': 'invalid_testpassw0rd123'
            }
        ]

        for input_data in input_data_list:
            serializer = LoginSerializer(data=input_data)
            self.assertFalse(serializer.is_valid())
