from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

User = get_user_model()


class PasswordChangeAPIViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(username='password_changeapiview',
                                 email='password_changeapiview@test.com',
                                 password='testpassw0rd123')

    def test_1_success_update_password(self):
        # 適切なパラメータによってユーザのパスワードを更新する事が出来る
        params = {
            'old_password': 'testpassw0rd123',
            'password': 'updatetestpassw0rd123',
            'password2': 'updatetestpassw0rd123',
        }

        user = User.objects.get(username='password_changeapiview')
        client = APIClient()
        client.force_login(user)
        response = client.patch(reverse('api:v1:users:change_password',
                                        kwargs={'username': 'password_changeapiview'}),
                                params,
                                format='json')
        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 200)
        # パスワードが更新されたか検証
        updated_user = User.objects.get(username='password_changeapiview')
        self.assertTrue(updated_user.check_password('updatetestpassw0rd123'))

    def test_2_fail_update_password(self):
        # 正しいパラメータであってもログインしていなければユーザのパスワードを更新する事が出来ない
        params = {
            'old_password': 'testpassw0rd123',
            'password': 'updatetestpassw0rd123',
            'password2': 'updatetestpassw0rd123',
        }

        client = APIClient()
        response = client.patch(reverse('api:v1:users:change_password',
                                        kwargs={'username': 'password_changeapiview'}),
                                params,
                                format='json')
        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 403)

    def test_3_fail_uppdate_password(self):
        # 誤ったパラメータまたは欠けたパラメータが存在する場合はユーザのパスワードを更新する事は出来ない
        wrong_params_list = [
            {
                'password': 'updatetestpassw0rd123',
                'password2': 'updatetestpassw0rd123',
            },
            {
                'old_password': 'testpassw0rd123',
                'password2': 'updatetestpassw0rd123',
            },
            {
                'old_password': 'testpassw0rd123',
                'password': 'updatetestpassw0rd123',
            },
            {
                'old_password': 'wrongpassword',
                'password': 'updatetestpassw0rd123',
                'password2': 'updatetestpassw0rd123',
            },
            {
                'old_password': 'testpassw0rd123',
                'password': 'wrongpassword',
                'password2': 'updatetestpassw0rd123',
            },
            {
                'old_password': 'testpassw0rd123',
                'password': 'updatetestpassw0rd123',
                'password2': 'wrongpassword',
            },
        ]

        user = User.objects.get(username='password_changeapiview')
        client = APIClient()
        client.force_login(user)

        for wrong_params in wrong_params_list:
            response = client.patch(reverse('api:v1:users:change_password',
                                            kwargs={'username': 'password_changeapiview'}),
                                    wrong_params,
                                    format='json')
            # HTTPレスポンスステータスコードの検証
            self.assertEqual(response.status_code, 400)
