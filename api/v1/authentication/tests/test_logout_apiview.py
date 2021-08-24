from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

User = get_user_model()


class LogoutAPIViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(username='logout_apiview',
                                 email='logout_apiview@test.com',
                                 password='testpassw0rd123')

    def test_success_logout(self):
        # ログアウト状態にする事が出来る
        user = User.objects.get(username='logout_apiview')
        client = APIClient()
        client.force_login(user)
        response = client.post(reverse('api:v1:authentication:logout'))
        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの確認
        expected_json_dict = {'detail': ['ログアウトに成功しました']}
        self.assertJSONEqual(response.content, expected_json_dict)
