from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class RegisterAPIViewTest(TestCase):
    def test_success_register(self):
        # 正しいユーザ情報によって認証を行う事が出来る
        params = {
            'username': 'register_apiview',
            'email': 'register_apiview@test.com',
            'password': 'testpassw0rd123',
            'password2': 'testpassw0rd123',
        }

        response = self.client.post(reverse('api:v1:authentication:register'),
                                    params,
                                    format='json')
        # ステータスコードの確認
        self.assertEqual(response.status_code, 201)
        # JSONレスポンスの確認
        expected_json_dict = {"username": "register_apiview"}
        self.assertJSONEqual(response.content, expected_json_dict)
        # Userオブジェクトが作成されたか確認
        created_user = User.objects.get(username='register_apiview')
        self.assertIsNotNone(created_user)
        # ユーザがログイン状態であるか確認
        self.assertTrue(created_user.is_authenticated)

    def test_fail_register(self):
        # ユーザ情報において誤った形式のフィールドが含まれる場合は登録する事が出来ない
        params_list = [
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

        for index, params in enumerate(params_list):
            response = self.client.post(reverse('api:v1:authentication:register'),
                                        params,
                                        format='json')
            # ステータスコードの確認
            self.assertEqual(response.status_code, 400)

            # JSONレスポンスの確認
            if index == 0:
                expected_json_dict = {'username': ['この項目が30文字より長くならないようにしてください。']}
            elif index == 1:
                expected_json_dict = {'email': ['有効なメールアドレスを入力してください。']}
            elif index == 2:
                expected_json_dict = {'password': ['入力されたパスワードが一致しません。']}

            self.assertJSONEqual(response.content, expected_json_dict)

    def test_fail_register2(self):
        # ユーザ情報において欠けたフィールドが含まれる場合は登録する事が出来ない
        params_list = [
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
            }
        ]

        for index, params in enumerate(params_list):
            response = self.client.post(reverse('api:v1:authentication:register'),
                                        params,
                                        format='json')
            # ステータスコードの確認
            self.assertEqual(response.status_code, 400)

            # JSONレスポンスの確認
            if index == 0:
                expected_json_dict = {'username': ['この項目は必須です。']}
            elif index == 1:
                expected_json_dict = {'email': ['この項目は必須です。']}
            elif index == 2:
                expected_json_dict = {'password': ['この項目は必須です。']}
            elif index == 3:
                expected_json_dict = {'password2': ['この項目は必須です。']}

            self.assertJSONEqual(response.content, expected_json_dict)
