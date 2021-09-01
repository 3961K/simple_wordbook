from django.contrib.auth import get_user_model
from django.urls import reverse
from urllib.parse import urlencode
from json import loads as json_loads
from rest_framework.test import APITestCase, APIClient

User = get_user_model()


class UserListAPIViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for i in range(1, 12):
            User.objects.create_user(username='user_listapiview_A{}'.format(i),
                                     email='user_listapiview_A{}@test.com'.format(i),
                                     password='testpassw0rd123')

            User.objects.create_user(username='user_listapiview_B{}'.format(i),
                                     email='user_listapiview_B{}@test.com'.format(i),
                                     password='testpassw0rd123')

        User.objects.create_user(username='user_listapiview_super',
                                 email='user_listapiview_super@test.com',
                                 is_superuser=True,
                                 password='testpassw0rd123')

        User.objects.create_user(username='user_listapiview_staff',
                                 email='user_listapiview_staff@test.com',
                                 is_staff=True,
                                 password='testpassw0rd123')

    def test_1_success_access_and_get_users(self):
        # APIViewに対してアクセスする事と10件の情報を取得する事が出来る
        client = APIClient()
        response = client.get(reverse('api:v1:users:list'))

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの確認 (取得件数を表すcountの値の比較によって確認を行う)
        response_json = json_loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['count'], 22)
        self.assertEqual(len(response_json['results']), 10)

    def test_2_success_access_max_page(self):
        # ページネーションが正常に機能し,最後のページの場合next=nullとなっている
        client = APIClient()
        response = client.get(''.join([reverse('api:v1:users:list'),
                                       '?',
                                       urlencode(dict(page='3'))]))

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの確認 (jsonオブジェクトに変換する過程でnullがNoneに変換されている)
        response_json = json_loads(response.content.decode('utf-8'))
        self.assertIsNone(response_json['next'])

    def test_3_success_get_only_satisfy_requirment(self):
        # qパラメータで指定した条件に合致する情報のみ取得する事可能で,
        # ページネーションも正常に機能している
        client = APIClient()
        response = client.get(''.join([reverse('api:v1:users:list'),
                                       '?',
                                       urlencode(dict(q='user_listapiview_A'))]))

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの確認 (取得件数を表すcountの値の比較によって確認を行う)
        response_json = json_loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['count'], 11)

    def test_4_fail_access_over_page(self):
        # ページネーションが正常に機能し,存在しないページにアクセスすると404が返ってくる
        client = APIClient()
        response = client.get(''.join([reverse('api:v1:users:list'),
                                       '?',
                                       urlencode(dict(page='4'))]))

        # ステータスコードの確認
        self.assertEqual(response.status_code, 404)
        # JSONレスポンスの確認
        expected_json = {'detail': '不正なページです。'}
        self.assertJSONEqual(response.content, expected_json)

    def test_5_fail_get_no_satisfy_requirment(self):
        # 条件に合致するデータが無い時,何も取得できない
        client = APIClient()
        response = client.get(''.join([reverse('api:v1:users:list'),
                                       '?',
                                       urlencode(dict(q='user_listapiview_C'))]))

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの確認
        response_json = json_loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['count'], 0)
