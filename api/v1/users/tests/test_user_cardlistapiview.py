from django.contrib.auth import get_user_model
from django.urls import reverse
from json import loads as json_loads
from rest_framework.test import APITestCase, APIClient
from urllib.parse import urlencode

from ...cards.models import Card

User = get_user_model()


class UserCardListAPIViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User(
            username='user_cardlistapiview',
            email='user_cardlistapiview@test.com',
            password='testpassw0rd123'
        )
        user.save()

        user2 = User(
            username='user_cardlistapiview2',
            email='user_cardlistapiview2@test.com',
            password='testpassw0rd123'
        )
        user2.save()

        for i in range(1, 12):
            is_hidden = False if i < 7 else True
            Card.objects.create(
                word='user_cardlistapiview_{}'.format(i),
                answer='user_cardlistapiview_{}'.format(i),
                is_hidden=is_hidden,
                author=user,
            )

    def test_1_success_get_list_with_authenticated_as_self(self):
        # アクセスしたユーザ名と同じユーザとして認証されている場合は非公開カード含む全ての
        # カードを取得する事が出来る
        user = User.objects.get(username='user_cardlistapiview')

        client = APIClient()
        client.force_login(user)
        response = client.get(reverse('api:v1:users:cards',
                                      kwargs={'username': user.username}))

        # HTTPレスポンスステータスコードの比較
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの比較
        json_response = json_loads(response.content)
        self.assertEqual(json_response['count'], 11)

        # ページングによるアクセスの検証
        for i in range(1, 3):
            response = client.get(''.join([reverse('api:v1:users:cards',
                                                   kwargs={'username': user.username}),
                                           '?',
                                           urlencode(dict(page=i))]))

            # HTTPレスポンスステータスコードの比較
            self.assertEqual(response.status_code, 200)
            # JSONレスポンスの比較
            json_response = json_loads(response.content)
            self.assertEqual(json_response['count'], 11)

    def test_2_success_get_list_with_authenticated_as_other(self):
        # アクセスしたユーザ名と異なるユーザとして認証されている場合は公開カードのみ取得する
        # 事が出来る
        user = User.objects.get(username='user_cardlistapiview')
        user2 = User.objects.get(username='user_cardlistapiview2')

        client = APIClient()
        client.force_login(user2)
        response = client.get(reverse('api:v1:users:cards',
                                      kwargs={'username': user.username}))

        # HTTPレスポンスステータスコードの比較
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの比較
        json_response = json_loads(response.content)
        self.assertEqual(json_response['count'], 6)

        # ページングによるアクセスの検証
        response = client.get(''.join([reverse('api:v1:users:cards',
                                               kwargs={'username': user.username}),
                                       '?',
                                       urlencode(dict(page='1'))]))

        # HTTPレスポンスステータスコードの比較
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの比較
        json_response = json_loads(response.content)
        self.assertEqual(json_response['count'], 6)

    def test_3_success_get_list_without_authenticated(self):
        # 認証されていない場合は公開カードのみ取得する事が出来る
        user = User.objects.get(username='user_cardlistapiview')

        client = APIClient()
        response = client.get(reverse('api:v1:users:cards',
                                      kwargs={'username': user.username}))

        # HTTPレスポンスステータスコードの比較
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの比較
        json_response = json_loads(response.content)
        self.assertEqual(json_response['count'], 6)

        # ページングによるアクセスの検証
        response = client.get(''.join([reverse('api:v1:users:cards',
                                               kwargs={'username': user.username}),
                                       '?',
                                       urlencode(dict(page='1'))]))

        # HTTPレスポンスステータスコードの比較
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの比較
        json_response = json_loads(response.content)
        self.assertEqual(json_response['count'], 6)

    def test_4_fail_get_list_over_page(self):
        # 存在しないページにアクセスする事は出来ない
        user = User.objects.get(username='user_cardlistapiview')

        client = APIClient()
        response = client.get(reverse('api:v1:users:cards',
                                      kwargs={'username': user.username}))

        # HTTPレスポンスステータスコードの比較 (認証されていない場合)
        response = client.get(''.join([reverse('api:v1:users:cards',
                                               kwargs={'username': user.username}),
                                       '?',
                                       urlencode(dict(page='2'))]))

        self.assertEqual(response.status_code, 404)

        # HTTPレスポンスステータスコードの比較 (異なるユーザとして認証されている場合)
        user2 = User.objects.get(username='user_cardlistapiview2')
        client.force_login(user2)
        response = client.get(''.join([reverse('api:v1:users:cards',
                                               kwargs={'username': user.username}),
                                       '?',
                                       urlencode(dict(page='2'))]))

        self.assertEqual(response.status_code, 404)

        # HTTPレスポンスステータスコードの比較 (自身として認証されている場合)
        client.force_login(user)
        response = client.get(''.join([reverse('api:v1:users:cards',
                                               kwargs={'username': user.username}),
                                       '?',
                                       urlencode(dict(page='3'))]))

        self.assertEqual(response.status_code, 404)
