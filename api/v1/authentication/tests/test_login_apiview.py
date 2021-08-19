from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class LoginAPIViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(username='login_apiview',
                                 email='login_apiview@test.com',
                                 password='testpassw0rd123')

    def test_success_authenticate(self):
        # 正しいユーザ情報によって認証を行う事が出来る
        params = {
            'username': 'login_apiview',
            'password': 'testpassw0rd123'
        }

        response = self.client.post(reverse('api:v1:authentication:login'),
                                    params,
                                    format='json')
        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの確認
        expected_json_dict = {'detail': ['ログインに成功しました']}
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_fail_authenticate(self):
        # 誤ったユーザ名・パスワードの組み合わせでは認証する事が出来ない
        params_list = [
            {
                'username': 'login_apiview',
                'password': 'invalid_testpassw0rd123'
            },
            {
                'username': 'invalid_login_apiview',
                'password': 'testpassw0rd123'
            },
        ]

        for params in params_list:
            # ステータスコードの確認
            response = self.client.post(reverse('api:v1:authentication:login'),
                                        params,
                                        format='json')
            self.assertEqual(response.status_code, 400)

            # JSONレスポンスの確認
            expected_json_dict = {'non_field_errors': ['ログインが失敗しました']}
            self.assertJSONEqual(response.content, expected_json_dict)

    def test_fail_authenticate2(self):
        # ユーザ名・パスワードどちらかが欠けた状態では認証する事が出来ない
        params_list = [
            {
                'username': 'login_apiview',
            },
            {
                'password': 'testpassw0rd123'
            },
        ]

        for index, params in enumerate(params_list):
            # ステータスコードの確認
            response = self.client.post(reverse('api:v1:authentication:login'),
                                        params,
                                        format='json')
            self.assertEqual(response.status_code, 400)

            # JSONレスポンスの確認
            if index == 0:
                expected_json_dict = {'password': ['この項目は必須です。']}
            elif index == 1:
                expected_json_dict = {'username': ['この項目は必須です。']}

            self.assertJSONEqual(response.content, expected_json_dict)
