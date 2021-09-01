from django.contrib.auth import get_user_model
from django.urls import reverse
from json import loads as json_loads
from rest_framework.test import APITestCase, APIClient
from urllib.parse import urlencode

from ..models import Card

User = get_user_model()


class CardListCreateAPIView(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User(username='card_listcreateapiview',
                    email='card_listcreateapiview_A{}@test.com',
                    password='testpassw0rd123')
        user.save()

        for i in range(1, 23):
            is_hidden = False if i <= 11 else True
            Card.objects.create(
                word='card_listcreateapiview_{}'.format(i),
                answer='card_listcreateapiview_{}'.format(i),
                is_hidden=is_hidden,
                author=user,
            )

    def test_1_success_get_list(self):
        # 公開状態のカードのリストを取得する事が出来る
        client = APIClient()
        response = client.get(reverse('api:v1:cards:list'))
        # HTTPステータスコードの検証
        self.assertEqual(response.status_code, 200)
        # 取得した件数の検証
        json_response = json_loads(response.content)
        self.assertEqual(json_response['count'], 11)
        self.assertEqual(len(json_response['results']), 10)

    def test_2_success_get_list_with_q(self):
        # qパラメータで指定した単語を含む公開状態のカードのリストを取得する事が出来る
        client = APIClient()
        response = client.get(''.join([reverse('api:v1:cards:list'),
                                       '?',
                                       urlencode(dict(q='1'))]))
        # HTTPステータスコードの検証
        self.assertEqual(response.status_code, 200)
        # 取得した件数の検証
        json_response = json_loads(response.content)
        self.assertEqual(json_response['count'], 3)
        self.assertEqual(len(json_response['results']), 3)

    def test_3_success_get_list_with_authenticated(self):
        # 認証された状態でアクセスした場合,自分が作成した非公開カードも取得する事が出来る
        user = User.objects.get(username='card_listcreateapiview')
        client = APIClient()
        client.force_login(user)
        response = client.get(reverse('api:v1:cards:list'))
        # HTTPステータスコードの検証
        self.assertEqual(response.status_code, 200)
        # 取得した件数の検証
        json_response = json_loads(response.content)
        self.assertEqual(json_response['count'], 22)
        self.assertEqual(len(json_response['results']), 10)

    def test_4_fail_get_list_with_q(self):
        # qパラメータで指定した単語を含む公開状態のカードが無い場合は何も取得できない (0件)
        client = APIClient()
        response = client.get(''.join([reverse('api:v1:cards:list'),
                                       '?',
                                      urlencode(dict(q='fail'))]))
        # HTTPステータスコードの検証
        self.assertEqual(response.status_code, 200)
        # 取得した件数の検証
        json_response = json_loads(response.content)
        self.assertEqual(len(json_response['results']), 0)

    def test_5_fail_access_over_page(self):
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

    def test_6_success_create(self):
        # 認証している状態で適切な値を送信する事でカードを新規作成する事が出来る
        params = {
            'word': 'success_create',
            'answer': 'success_create',
            'is_hidden': False,
        }

        user = User.objects.get(username='card_listcreateapiview')
        client = APIClient()
        client.force_login(user)
        response = client.post(reverse('api:v1:cards:list'),
                               params,
                               format='json')
        # HTTPレスポンスの検証
        self.assertEqual(response.status_code, 201)
        # JSONレスポンスの検証 (word, ansertの検証)
        json_response = json_loads(response.content)
        self.assertEqual(json_response['word'], 'success_create')
        self.assertEqual(json_response['answer'], 'success_create')

    def test_7_fail_create_unauthenticated(self):
        # 認証されていなければ適切な値でもカードを新規作成する事は出来ない
        params = {
            'word': 'fail_create',
            'answer': 'fail_create',
            'is_hidden': False,
        }

        client = APIClient()
        response = client.post(reverse('api:v1:cards:list'),
                               params,
                               format='json')
        # HTTPレスポンスの検証
        self.assertEqual(response.status_code, 403)

    def test_8_fail_create_wrong_params(self):
        # 認証されていても不適切な値の場合カードを新規作成する事は出来ない
        wrong_params_list = [
            {
                'word': 'A' * 101,
                'answer': 'success_create',
                'is_hidden': False,
            },
            {
                'word': 'success_create',
                'answer': 'A' * 201,
                'is_hidden': False,
            }
        ]

        user = User.objects.get(username='card_listcreateapiview')
        client = APIClient()
        client.force_login(user)
        for wrong_params in wrong_params_list:
            response = client.post(reverse('api:v1:cards:list'),
                                   wrong_params,
                                   format='json')
            # HTTPレスポンスの検証
            self.assertEqual(response.status_code, 400)
