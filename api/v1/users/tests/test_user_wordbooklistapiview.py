from django.contrib.auth import get_user_model
from django.urls import reverse
from json import loads as json_loads
from rest_framework.test import APITestCase, APIClient
from urllib.parse import urlencode

from ...wordbooks.models import Wordbook

User = get_user_model()


class UserWordbookListAPIViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User(
            username='user_wordbooklistapiview',
            email='user_wordbooklistapiview@test.com',
            password='testpassw0rd123'
        )
        user.save()

        user2 = User(
            username='user_wordbooklistapiview2',
            email='user_wordbooklistapiview2@test.com',
            password='testpassw0rd123'
        )
        user2.save()

        for i in range(1, 12):
            is_hidden = False if i < 7 else True
            Wordbook.objects.create(
                wordbook_name='user_wordbooklistapiview_{}'.format(i),
                is_hidden=is_hidden,
                author=user,
            )

    def test_1_success_get_list_with_authenticated_as_self(self):
        # アクセスしたユーザ名と同じユーザとして認証されている場合は非公開単語帳含む全ての
        # 単語帳を取得する事が出来る
        user = User.objects.get(username='user_wordbooklistapiview')

        client = APIClient()
        client.force_login(user)
        response = client.get(reverse('api:v1:users:wordbooks',
                                      kwargs={'username': user.username}))

        # HTTPレスポンスステータスコードの比較
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの比較
        json_response = json_loads(response.content)
        self.assertEqual(json_response['count'], 11)

        # ページングによるアクセスの検証
        for i in range(1, 3):
            response = client.get(''.join([reverse('api:v1:users:wordbooks',
                                                   kwargs={'username': user.username}),
                                           '?',
                                           urlencode(dict(page=i))]))

            # HTTPレスポンスステータスコードの比較
            self.assertEqual(response.status_code, 200)
            # JSONレスポンスの比較
            json_response = json_loads(response.content)
            self.assertEqual(json_response['count'], 11)

    def test_2_success_get_list_with_authenticated_as_other(self):
        # アクセスしたユーザ名と異なるユーザとして認証されている場合は公開単語帳のみ取得する
        # 事が出来る
        user = User.objects.get(username='user_wordbooklistapiview')
        user2 = User.objects.get(username='user_wordbooklistapiview2')

        client = APIClient()
        client.force_login(user2)
        response = client.get(reverse('api:v1:users:wordbooks',
                                      kwargs={'username': user.username}))

        # HTTPレスポンスステータスコードの比較
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの比較
        json_response = json_loads(response.content)
        self.assertEqual(json_response['count'], 6)

        # ページングによるアクセスの検証
        response = client.get(''.join([reverse('api:v1:users:wordbooks',
                                               kwargs={'username': user.username}),
                                       '?',
                                       urlencode(dict(page='1'))]))

        # HTTPレスポンスステータスコードの比較
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの比較
        json_response = json_loads(response.content)
        self.assertEqual(json_response['count'], 6)

    def test_3_success_get_list_without_authenticated(self):
        # 認証されていない場合は公開単語帳のみ取得する事が出来る
        user = User.objects.get(username='user_wordbooklistapiview')

        client = APIClient()
        response = client.get(reverse('api:v1:users:wordbooks',
                                      kwargs={'username': user.username}))

        # HTTPレスポンスステータスコードの比較
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの比較
        json_response = json_loads(response.content)
        self.assertEqual(json_response['count'], 6)

        # ページングによるアクセスの検証
        response = client.get(''.join([reverse('api:v1:users:wordbooks',
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
        user = User.objects.get(username='user_wordbooklistapiview')

        client = APIClient()
        response = client.get(reverse('api:v1:users:wordbooks',
                                      kwargs={'username': user.username}))

        # HTTPレスポンスステータスコードの比較 (認証されていない場合)
        response = client.get(''.join([reverse('api:v1:users:wordbooks',
                                               kwargs={'username': user.username}),
                                       '?',
                                       urlencode(dict(page='2'))]))

        self.assertEqual(response.status_code, 404)

        # HTTPレスポンスステータスコードの比較 (異なるユーザとして認証されている場合)
        user2 = User.objects.get(username='user_wordbooklistapiview2')
        client.force_login(user2)
        response = client.get(''.join([reverse('api:v1:users:wordbooks',
                                               kwargs={'username': user.username}),
                                       '?',
                                       urlencode(dict(page='2'))]))

        self.assertEqual(response.status_code, 404)

        # HTTPレスポンスステータスコードの比較 (自身として認証されている場合)
        client.force_login(user)
        response = client.get(''.join([reverse('api:v1:users:wordbooks',
                                               kwargs={'username': user.username}),
                                       '?',
                                       urlencode(dict(page='3'))]))

        self.assertEqual(response.status_code, 404)
