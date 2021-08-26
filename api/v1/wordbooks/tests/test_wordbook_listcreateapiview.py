from django.contrib.auth import get_user_model
from django.urls import reverse
from json import loads as json_loads
from rest_framework.test import APITestCase, APIClient
from urllib.parse import urlencode

from ..models import Wordbook

User = get_user_model()


class WordbookListCreateAPIView(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User(username='wordbook_listcreateapiview',
                    email='card_listcreateapiview_A{}@test.com',
                    password='testpassw0rd123')
        user.save()

        for i in range(1, 13):
            is_hidden = False if i <= 11 else True
            Wordbook.objects.create(
                wordbook_name='wordbook_listcreateapiview_{}'.format(i),
                is_hidden=is_hidden,
                author=user,
            )

    def test_1_success_get_list(self):
        # 公開状態の単語帳のリストを取得する事が出来る
        client = APIClient()
        response = client.get(reverse('api:v1:wordbooks:list'))
        # HTTPステータスコードの検証
        self.assertEqual(response.status_code, 200)
        # 取得した件数の検証
        json_response = json_loads(response.content)
        self.assertEqual(len(json_response['results']), 10)

    def test_2_success_get_list_with_q(self):
        # qパラメータで指定した単語を含む公開状態の単語帳のリストを取得する事が出来る
        client = APIClient()
        response = client.get(''.join([reverse('api:v1:wordbooks:list'),
                                       '?',
                                       urlencode(dict(q='1'))]))
        # HTTPステータスコードの検証
        self.assertEqual(response.status_code, 200)
        # 取得した件数の検証
        json_response = json_loads(response.content)
        self.assertEqual(len(json_response['results']), 3)

    def test_3_fail_get_list_with_q(self):
        # qパラメータで指定した単語を含む公開状態の単語帳が無い場合は何も取得できない (0件)
        client = APIClient()
        response = client.get(''.join([reverse('api:v1:wordbooks:list'),
                                       '?',
                                       urlencode(dict(q='fail'))]))
        # HTTPステータスコードの検証
        self.assertEqual(response.status_code, 200)
        # 取得した件数の検証
        json_response = json_loads(response.content)
        self.assertEqual(len(json_response['results']), 0)

    def test_4_fail_access_over_page(self):
        # ページネーションが正常に機能し,存在しないページにアクセスすると404が返ってくる
        client = APIClient()
        response = client.get(''.join([reverse('api:v1:cards:list'),
                                       '?',
                                       urlencode(dict(page='3'))]))
        # HTTPステータスコードの検証
        self.assertEqual(response.status_code, 404)
        # JSONレスポンスの確認
        expected_json = {'detail': '不正なページです。'}
        self.assertJSONEqual(response.content, expected_json)

    def test_5_success_create(self):
        # 認証している状態で適切な値を送信する事で単語帳を新規作成する事が出来る
        params = {
            'wordbook_name': 'success_create',
            'is_hidden': False,
        }

        user = User.objects.get(username='wordbook_listcreateapiview')
        client = APIClient()
        client.force_login(user)
        response = client.post(reverse('api:v1:wordbooks:list'),
                               params,
                               format='json')
        # HTTPレスポンスの検証
        self.assertEqual(response.status_code, 201)
        # JSONレスポンスの検証 (wordbook_nameの検証)
        json_response = json_loads(response.content)
        self.assertEqual(json_response['wordbook_name'], 'success_create')

    def test_6_fail_create_unauthenticated(self):
        # 認証されていなければ適切な値でも単語帳を新規作成する事は出来ない
        params = {
            'wordbook_name': 'fail_create',
            'is_hidden': False,
        }

        client = APIClient()
        response = client.post(reverse('api:v1:wordbooks:list'),
                               params,
                               format='json')
        # HTTPレスポンスの検証
        self.assertEqual(response.status_code, 403)

    def test_7_fail_create_wrong_params(self):
        # 認証されていても不適切な値の場合カードを新規作成する事は出来ない
        wrong_params_list = [
            {
                'wordbook_name': 'A' * 101,
                'is_hidden': False,
            },
            {
                'wordbook_name': 'fail_create',
                'is_hidden': 'wrong',
            }
        ]

        user = User.objects.get(username='wordbook_listcreateapiview')
        client = APIClient()
        client.force_login(user)
        for wrong_params in wrong_params_list:
            response = client.post(reverse('api:v1:wordbooks:list'),
                                   wrong_params,
                                   format='json')
            # HTTPレスポンスの検証
            self.assertEqual(response.status_code, 400)
