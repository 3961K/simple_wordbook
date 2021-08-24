from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from ..serializers import PasswordChangeSerializer

User = get_user_model()


class PasswordChangeSerializerTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(
            username='password_changeserializer',
            email='password_changeserializer@test.com',
            password='testpassw0rd123',)

    def test_1_valid_and_success_update(self):
        # 正しい入力値は妥当であり,それによってパスワードを更新する事が出来る
        user = User.objects.get(username='password_changeserializer')
        params = {
            'old_password': 'testpassw0rd123',
            'password': 'updatedtestpassw0rd123',
            'password2': 'updatedtestpassw0rd123'
        }

        serializer = PasswordChangeSerializer(instance=user,
                                              data=params,
                                              user=user)
        # バリデーション結果の検証
        self.assertTrue(serializer.is_valid())
        serializer.update(user, serializer.validated_data)
        # パスワードが更新されたか検証
        self.assertTrue(user.check_password('updatedtestpassw0rd123'))

    def test_2_invalid(self):
        # 誤った入力値または欠けた状態は妥当ではない
        user = User.objects.get(username='password_changeserializer')
        invalid_params_list = [
            {
                'password': 'updatedtestpassw0rd123',
                'password2': 'updatedtestpassw0rd123'
            },
            {
                'old_password': 'wrongpass',
                'password2': 'updatedtestpassw0rd123'
            },
            {
                'old_password': 'wrongpass',
                'password': 'updatedtestpassw0rd123',
            },
            {
                'old_password': 'wrongpass',
                'password': 'updatedtestpassw0rd123',
                'password2': 'updatedtestpassw0rd123'
            },
            {
                'old_password': 'testpassw0rd123',
                'password': 'wrongpass',
                'password2': 'updatedtestpassw0rd123'
            },

            {
                'old_password': 'testpassw0rd123',
                'password': 'updatedtestpassw0rd123',
                'password2': 'wrongpass'
            },
        ]

        for invalid_params in invalid_params_list:
            serializer = PasswordChangeSerializer(instance=user,
                                                  data=invalid_params,
                                                  user=user)
            # バリデーション結果の検証
            self.assertFalse(serializer.is_valid())
