from django.contrib.auth import get_user_model
from django.urls import reverse
from json import loads as json_loads
from rest_framework.test import APITestCase, APIClient
from urllib.parse import urlencode

from ..models import Wordbook
from ...cards.models import Card

User = get_user_model()


class WordbookCardListAPIView(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User(username='wordbook_cards_listapiview',
                    email='wordbook_cards_listapiview@test.com',
                    password='testpassw0rd123')
        user.save()

        user2 = User(username='wordbook_cards_listapiview2',
                     email='wordbook_cards_listapiview2@test.com',
                     password='testpassw0rd123')
        user2.save()

        wordbook = Wordbook(
            wordbook_name='wordbook_cards_listapiview_public',
            author=user
        )
        wordbook.save()

        wordbook2 = Wordbook(
            wordbook_name='wordbook_cards_listapiview_private',
            is_hidden=True,
            author=user
        )
        wordbook2.save()

        for i in range(1, 23):
            is_hidden = True if i < 12 else False
            card = Card(
                word='wordbook_cards_listapiview_{}'.format(i),
                answer='wordbook_cards_listapiview_{}'.format(i),
                is_hidden=is_hidden,
                author=user,
            )
            card.wordbooks.add(wordbook)
            card.wordbooks.add(wordbook2)
            card.save()

    def test_1_success_get_list_with_authenticated(self):
        # 単語帳の作者として認証されている場合は非公開カードを含んだ全てのカードを取得する事
        # が出来る
        user = User.objects.get(username='wordbook_cards_listapiview')

        wordbook = Wordbook.objects.get(
            wordbook_name='wordbook_cards_listapiview_public')

        client = APIClient()
        client.force_login(user)

        response = client.get(reverse('api:v1:wordbooks:cards',
                                      kwargs={'id': wordbook.id}))

        # ステータスコードの検証
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの検証
        json_response = json_loads(response.content)
        self.assertEqual(json_response['count'], 22)

        # ページを指定したアクセスの確認
        for i in range(1, 4):
            response = client.get(''.join([reverse('api:v1:wordbooks:cards',
                                                   kwargs={'id': wordbook.id}),
                                           '?',
                                           urlencode(dict(page=i))]))
            # ステータスコードの検証
            self.assertEqual(response.status_code, 200)
            # JSONレスポンスの検証
            json_response = json_loads(response.content)
            self.assertEqual(json_response['count'], 22)

    def test_2_success_get_list_without_authenticated(self):
        # 別のユーザとして認証されている場合は公開カードのみを取得する事が出来る
        wordbook = Wordbook.objects.get(
            wordbook_name='wordbook_cards_listapiview_public')

        client = APIClient()
        response = client.get(reverse('api:v1:wordbooks:cards',
                                      kwargs={'id': wordbook.id}))

        # ステータスコードの検証
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの検証
        json_response = json_loads(response.content)
        self.assertEqual(json_response['count'], 11)

        # ページを指定したアクセスの確認
        for i in range(1, 3):
            response = client.get(''.join([reverse('api:v1:wordbooks:cards',
                                                   kwargs={'id': wordbook.id}),
                                           '?',
                                           urlencode(dict(page=i))]))
            # ステータスコードの検証
            self.assertEqual(response.status_code, 200)
            # JSONレスポンスの検証
            json_response = json_loads(response.content)
            self.assertEqual(json_response['count'], 11)

    def test_3_success_get_hidden_list_with_authenticated_as_author(self):
        # authorとして認証されている場合は非公開の単語帳にアクセスする事が出来る
        user = User.objects.get(username='wordbook_cards_listapiview')

        wordbook = Wordbook.objects.get(
            wordbook_name='wordbook_cards_listapiview_private')

        client = APIClient()
        client.force_login(user)

        response = client.get(reverse('api:v1:wordbooks:cards',
                                      kwargs={'id': wordbook.id}))

        # ステータスコードの検証
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの検証
        json_response = json_loads(response.content)
        self.assertEqual(json_response['count'], 22)

        # ページを指定したアクセスの確認
        for i in range(1, 4):
            response = client.get(''.join([reverse('api:v1:wordbooks:cards',
                                                   kwargs={'id': wordbook.id}),
                                           '?',
                                           urlencode(dict(page=i))]))
            # ステータスコードの検証
            self.assertEqual(response.status_code, 200)
            # JSONレスポンスの検証
            json_response = json_loads(response.content)
            self.assertEqual(json_response['count'], 22)

    def test_4_fail_get_list_over_page(self):
        # 範囲外のページへはアクセスする事は出来ない
        user = User.objects.get(username='wordbook_cards_listapiview')

        wordbook = Wordbook.objects.get(
            wordbook_name='wordbook_cards_listapiview_private')

        client = APIClient()
        client.force_login(user)

        response = client.get(reverse('api:v1:wordbooks:cards',
                                      kwargs={'id': wordbook.id}))

        response = client.get(''.join([reverse('api:v1:wordbooks:cards',
                                               kwargs={'id': wordbook.id}),
                                       '?',
                                       urlencode(dict(page='4'))]))
        # ステータスコードの検証
        self.assertEqual(response.status_code, 404)

    def test_5_fail_get_list_with_authenticated_as_otheruser(self):
        # 非公開の単語帳にはauthorと異なるユーザとしてログインしている場合では取得する事が
        # 出来ない
        user = User.objects.get(username='wordbook_cards_listapiview2')

        wordbook = Wordbook.objects.get(
            wordbook_name='wordbook_cards_listapiview_private')

        client = APIClient()
        client.force_login(user)

        response = client.get(reverse('api:v1:wordbooks:cards',
                                      kwargs={'id': wordbook.id}))
        # ステータスコードの検証
        self.assertEqual(response.status_code, 403)

    def test_6_fail_get_list_without_authenticated(self):
        # 非公開の単語帳にはログインしていない場合は取得する事が出来ない
        wordbook = Wordbook.objects.get(
            wordbook_name='wordbook_cards_listapiview_private')

        client = APIClient()

        response = client.get(reverse('api:v1:wordbooks:cards',
                                      kwargs={'id': wordbook.id}))
        # ステータスコードの検証
        self.assertEqual(response.status_code, 403)
