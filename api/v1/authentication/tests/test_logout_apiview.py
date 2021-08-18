from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class LogoutAPIViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        User.objects.create_user(username='logout_apiview',
                                 email='logout_apiview@test.com',
                                 password='testpassw0rd123')
        return super().setUpClass()

    def test_success_logout(self):
        # ログアウト状態にする事が出来る
        user = User.objects.get(username='logout_apiview')
        self.client.force_login(user)
        response = self.client.post(reverse('api:v1:authentication:logout'))
        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの確認
        expected_json_dict = {'detail': ['ログアウトに成功しました']}
        self.assertJSONEqual(response.content, expected_json_dict)
