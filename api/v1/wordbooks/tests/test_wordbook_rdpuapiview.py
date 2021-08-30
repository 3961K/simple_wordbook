from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from json import loads as json_loads
from rest_framework.test import APITestCase, APIClient

from ..models import Wordbook
from ...cards.models import Card

User = get_user_model()


class WordbookRetrieveDeletePartialUpdateAPIViewTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create(
            username='wordbook_rdpuapiview',
            email='wordbook_rdpuapiview@test.com',
            password='testpassw0rd123',
        )
        user.save()

        user2 = User.objects.create(
            username='wordbook_rdpuapiview2',
            email='wordbook_rdpuapiview2@test.com',
            password='testpassw0rd123',
        )
        user2.save()

        card = Card(
            word='wordbook_rdpuapiview',
            answer='wordbook_rdpuapiview',
            author=user,
        )
        card.save()

        card2 = Card(
            word='wordbook_rdpuapiview2',
            answer='wordbook_rdpuapiview2',
            author=user,
        )
        card2.save()

        wordbook = Wordbook(
            wordbook_name='wordbook_rdpuapiview_public',
            is_hidden=False,
            author=user,
        )
        wordbook.cards.add(card)
        wordbook.save()

        Wordbook.objects.create(
            wordbook_name='wordbook_rdpuapiview_private',
            is_hidden=True,
            author=user,
        )

        wordbook2 = Wordbook(
            wordbook_name='wordbook_rdpuapiview2_public',
            is_hidden=False,
            author=user2,
        )
        wordbook2.cards.add(card2)
        wordbook2.save()

        Wordbook.objects.create(
            wordbook_name='wordbook_rdpuapiview2_private',
            is_hidden=True,
            author=user2,
        )

    def test_1_success_retrive(self):
        # 指定した単語帳の詳細情報を取得する事が出来る
        wordbook = Wordbook.objects.get(wordbook_name='wordbook_rdpuapiview_public')
        client = APIClient()
        response = client.get(reverse('api:v1:wordbooks:detail',
                                      kwargs={'id': wordbook.id}))

        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 200)
        # HTTPレスポンスの検証
        json_response = json_loads(response.content)
        self.assertEqual(len(json_response.keys()), 5)
        self.assertEqual(json_response['wordbook_name'], 'wordbook_rdpuapiview_public')
        self.assertEqual(json_response['author_name'], 'wordbook_rdpuapiview')
        self.assertFalse(json_response['is_hidden'])
        self.assertIsNotNone(json_response['id'])
        self.assertIsNotNone(json_response['create_date'])

    def test_2_fail_retrive_no_exist(self):
        # 存在しない単語帳の詳細情報を取得しようとすると404が返ってくる
        client = APIClient()
        response = client.get(reverse('api:v1:wordbooks:detail',
                                      kwargs={'id': '00000000-0000-0000-0000-000000000000'}))

        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 404)

    def test_3_success_retrive_hidden(self):
        # 非公開単語帳はその作者として認証されている状態でアクセスした場合は取得できる
        wordbook = Wordbook.objects.get(wordbook_name='wordbook_rdpuapiview_private')
        user = User.objects.get(username='wordbook_rdpuapiview')

        client = APIClient()
        client.force_login(user)
        response = client.get(reverse('api:v1:wordbooks:detail',
                                      kwargs={'id': wordbook.id}))

        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 200)
        # HTTPレスポンスの検証
        json_response = json_loads(response.content)
        self.assertEqual(len(json_response.keys()), 5)
        self.assertEqual(json_response['wordbook_name'], 'wordbook_rdpuapiview_private')
        self.assertEqual(json_response['author_name'], 'wordbook_rdpuapiview')
        self.assertTrue(json_response['is_hidden'])
        self.assertIsNotNone(json_response['id'])
        self.assertIsNotNone(json_response['create_date'])

    def test_4_fail_retrive_hidden_unauthorization(self):
        # 非公開単語帳は認証されていない状態でアクセスした場合は取得できない
        wordbook = Wordbook.objects.get(wordbook_name='wordbook_rdpuapiview_private')

        client = APIClient()
        response = client.get(reverse('api:v1:wordbooks:detail',
                                      kwargs={'id': wordbook.id}))

        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 403)

    def test_5_fail_retrive_hidden_otheruser(self):
        # 非公開単語帳は作者以外のユーザとして認証されている状態でアクセスした場合は取得できない
        wordbook = Wordbook.objects.get(wordbook_name='wordbook_rdpuapiview_private')
        user = User.objects.get(username='wordbook_rdpuapiview2')

        client = APIClient()
        client.force_login(user)
        response = client.get(reverse('api:v1:wordbooks:detail',
                                      kwargs={'id': wordbook.id}))

        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 403)

    def test_6_success_update(self):
        # その単語帳のauthorとしてログインしている場合は適切な入力値で単語帳の
        # wordbook_name, is_hidden, 格納されているカードを更新する事が出来る
        wordbook = Wordbook.objects.get(wordbook_name='wordbook_rdpuapiview_public')
        user = User.objects.get(username='wordbook_rdpuapiview')

        card = Card.objects.get(word='wordbook_rdpuapiview')
        card2 = Card.objects.get(word='wordbook_rdpuapiview2')

        params = {
            'wordbook_name': 'update_wordbook_rdpuapiview_public',
            'is_hidden': True,
            'add_cards': [card2.id],
            'delete_cards': [card.id],
        }

        client = APIClient()
        client.force_login(user)
        response = client.patch(reverse('api:v1:wordbooks:detail',
                                        kwargs={'id': wordbook.id}),
                                params,
                                format='json')
        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 200)
        # 単語帳が更新されたか検証
        updated_wordbook = Wordbook.objects.get(id=wordbook.id)
        self.assertFalse(card in updated_wordbook.cards.all())
        self.assertTrue(card2 in updated_wordbook.cards.all())

    def test_7_fail_update_unauthorization(self):
        # 認証されていない場合は適切な入力値でもカードのword,answer,is_hiddenを
        # 更新する事が出来ない (403が返ってくる)
        wordbook = Wordbook.objects.get(wordbook_name='wordbook_rdpuapiview_public')
        user = User.objects.get(username='wordbook_rdpuapiview2')

        card = Card.objects.get(word='wordbook_rdpuapiview')
        card2 = Card.objects.get(word='wordbook_rdpuapiview2')

        params = {
            'wordbook_name': 'update_wordbook_rdpuapiview_public',
            'is_hidden': True,
            'add_cards': [card2.id],
            'delete_cards': [card.id],
        }

        client = APIClient()
        client.force_login(user)
        response = client.patch(reverse('api:v1:wordbooks:detail',
                                        kwargs={'id': wordbook.id}),
                                params,
                                format='json')
        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 403)

    def test_8_fail_update_other_user(self):
        # author以外のユーザとして認証されている場合は適切な入力値でも単語帳の情報を
        # を更新する事が出来ない (403が返ってくる)
        wordbook = Wordbook.objects.get(wordbook_name='wordbook_rdpuapiview_public')

        card = Card.objects.get(word='wordbook_rdpuapiview')
        card2 = Card.objects.get(word='wordbook_rdpuapiview2')

        params = {
            'wordbook_name': 'update_wordbook_rdpuapiview_public',
            'is_hidden': True,
            'add_cards': [card2.id],
            'delete_cards': [card.id],
        }

        client = APIClient()
        response = client.patch(reverse('api:v1:wordbooks:detail',
                                        kwargs={'id': wordbook.id}),
                                params,
                                format='json')
        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 403)

    def test_9_fail_update_wrong_params(self):
        # その単語帳のauthorとしてログインしている場合でも不適切な入力値では
        # 単語帳のwordとanswerを更新する事が出来ない (400が返ってくる)
        wordbook = Wordbook.objects.get(wordbook_name='wordbook_rdpuapiview_public')
        user = User.objects.get(username='wordbook_rdpuapiview')

        card = Card.objects.get(word='wordbook_rdpuapiview')
        card2 = Card.objects.get(word='wordbook_rdpuapiview2')

        wrong_params_list = [
            {
                'wordbook_name': 'A' * 101,
                'is_hidden': True,
                'add_cards': [card2.id],
                'delete_cards': [card.id],
            },
            {
                'wordbook_name': 'update_wordbook_rdpuapiview_public',
                'is_hidden': 'wrong_param',
                'add_cards': [card2.id],
                'delete_cards': [card.id],
            },
            {
                'wordbook_name': 'update_wordbook_rdpuapiview_public',
                'is_hidden': True,
                'add_cards': ['wrong_param'],
                'delete_cards': [card.id],
            },
            {
                'wordbook_name': 'update_wordbook_rdpuapiview_public',
                'is_hidden': True,
                'add_cards': [card2.id],
                'delete_cards': ['wrong_param'],
            }
        ]

        client = APIClient()
        client.force_login(user)

        for wrong_param in wrong_params_list:
            response = client.patch(reverse('api:v1:wordbooks:detail',
                                            kwargs={'id': wordbook.id}),
                                    wrong_param,
                                    format='json')
            # HTTPレスポンスステータスコードの検証
            self.assertEqual(response.status_code, 400)

    def test_10_success_delete(self):
        # その単語帳のauthorとしてログインしている場合はその単語帳を削除できる
        # (204が返ってくる)
        wordbook = Wordbook.objects.get(wordbook_name='wordbook_rdpuapiview_public')
        user = User.objects.get(username='wordbook_rdpuapiview')

        client = APIClient()
        client.force_login(user)
        response = client.delete(reverse('api:v1:wordbooks:detail',
                                         kwargs={'id': wordbook.id}))
        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 204)
        # 単語帳が削除されたか検証
        with self.assertRaises(ObjectDoesNotExist):
            wordbook = Wordbook.objects.get(wordbook_name='wordbook_rdpuapiview_public')

    def test_11_fail_update_unauthorization(self):
        # 認証されていない場合はその単語帳を削除する事は出来ない
        wordbook = Wordbook.objects.get(wordbook_name='wordbook_rdpuapiview_public')

        client = APIClient()
        response = client.delete(reverse('api:v1:wordbooks:detail',
                                         kwargs={'id': wordbook.id}))
        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 403)

    def test_12_fail_update_other_user(self):
        # author以外のユーザとして認証されている場合はその単語帳を削除する事は出来ない
        wordbook = Wordbook.objects.get(wordbook_name='wordbook_rdpuapiview_public')
        user = User.objects.get(username='wordbook_rdpuapiview2')

        client = APIClient()
        client.force_login(user)
        response = client.delete(reverse('api:v1:wordbooks:detail',
                                         kwargs={'id': wordbook.id}))
        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 403)
