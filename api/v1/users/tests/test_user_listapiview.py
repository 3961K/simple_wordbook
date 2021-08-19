from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from urllib.parse import urlencode
from json import loads as json_loads

User = get_user_model()


class UserListAPIViewTest(TestCase):
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

    def test_success_access_and_get_users(self):
        # エンドポイントに対してアクセスする事と10件の情報を取得する事が出来る
        response = self.client.get(reverse('api:v1:users:list'))

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの確認 (取得件数を表すcountの値の比較によって確認を行う)
        response_json = json_loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['count'], 22)

    def test_success_access_max_page(self):
        # ページネーションが正常に機能し,最後のページの場合next=nullとなっている
        response = self.client.get(''.join([reverse('api:v1:users:list'),
                                           '?',
                                            urlencode(dict(page='3'))]))

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの確認 (jsonオブジェクトに変換する過程でnullがNoneに変換されている)
        response_json = json_loads(response.content.decode('utf-8'))
        self.assertIsNone(response_json['next'])

    def test_success_get_only_satisfy_requirment(self):
        # qパラメータで指定した条件に合致する情報のみ取得する事可能で,
        # ページネーションも正常に機能している
        response = self.client.get(''.join([reverse('api:v1:users:list'),
                                           '?',
                                            urlencode(dict(q='user_listapiview_A'))]))

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの確認 (取得件数を表すcountの値の比較によって確認を行う)
        response_json = json_loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['count'], 11)

    def test_fail_access_over_page(self):
        # ページネーションが正常に機能し,存在しないページにアクセスすると404が返ってくる
        response = self.client.get(''.join([reverse('api:v1:users:list'),
                                           '?',
                                            urlencode(dict(page='4'))]))

        # ステータスコードの確認
        self.assertEqual(response.status_code, 404)
        # JSONレスポンスの確認
        expected_json = {'detail': '不正なページです。'}
        self.assertJSONEqual(response.content, expected_json)

    def test_fail_get_no_satisfy_requirment(self):
        # 条件に合致するデータが無い時,何も取得できない
        response = self.client.get(''.join([reverse('api:v1:users:list'),
                                           '?',
                                            urlencode(dict(q='user_listapiview_C'))]))

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの確認
        response_json = json_loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['count'], 0)
