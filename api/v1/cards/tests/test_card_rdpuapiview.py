from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from json import loads as json_loads
from rest_framework.test import APITestCase, APIClient

from ..models import Card

User = get_user_model()


class CardRetrieveDeletePartialUpdateAPIView(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create(
            username='card_rdpuapiview',
            email='card_rdpuapiview@test.com',
            password='testpassw0rd123',
        )
        user.save()

        user2 = User.objects.create(
            username='card_rdpuapiview2',
            email='card_rdpuapiview2@test.com',
            password='testpassw0rd123',
        )
        user2.save()

        Card.objects.create(
            word='card_rdpuapiview',
            answer='card_rdpuapiview',
            is_hidden=False,
            author=user
        )

        Card.objects.create(
            word='card_rdpuapiview2',
            answer='card_rdpuapiview2',
            is_hidden=True,
            author=user2
        )

    def test_1_success_retrive(self):
        # 指定したカードの詳細情報を取得する事が出来る
        card = Card.objects.get(word='card_rdpuapiview')
        client = APIClient()
        response = client.get(reverse('api:v1:cards:detail',
                                      kwargs={'id': card.id}))

        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 200)
        # HTTPレスポンスの検証
        json_response = json_loads(response.content)
        self.assertEqual(len(json_response.keys()), 5)
        self.assertEqual(json_response['word'], 'card_rdpuapiview')
        self.assertEqual(json_response['answer'], 'card_rdpuapiview')
        self.assertFalse(json_response['is_hidden'])
        self.assertIsNotNone(json_response['id'])
        self.assertIsNotNone(json_response['create_date'])

    def test_2_fail_retrive_no_exist(self):
        # 存在しないカードの詳細情報を取得しようとすると404が返ってくる
        client = APIClient()
        response = client.get(reverse('api:v1:cards:detail',
                                      kwargs={'id': '00000000-0000-0000-0000-000000000000'}))

        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 404)

    def test_3_success_retrive_hidden(self):
        # 非公開カードはその作者として認証されている状態でアクセスした場合は取得できる
        card = Card.objects.get(word='card_rdpuapiview2')
        user = User.objects.get(username='card_rdpuapiview2')

        client = APIClient()
        client.force_login(user)
        response = client.get(reverse('api:v1:cards:detail',
                                      kwargs={'id': card.id}))

        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 200)
        # HTTPレスポンスの検証
        json_response = json_loads(response.content)
        self.assertEqual(len(json_response.keys()), 5)
        self.assertEqual(json_response['word'], 'card_rdpuapiview2')
        self.assertEqual(json_response['answer'], 'card_rdpuapiview2')
        self.assertTrue(json_response['is_hidden'])
        self.assertIsNotNone(json_response['id'])
        self.assertIsNotNone(json_response['create_date'])

    def test_4_fail_retrive_hidden_unauthorization(self):
        # 非公開カードは認証されていない状態でアクセスした場合は取得できない
        card = Card.objects.get(word='card_rdpuapiview2')
        client = APIClient()
        response = client.get(reverse('api:v1:cards:detail',
                                      kwargs={'id': card.id}))

        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 403)

    def test_5_fail_retrive_hidden_otheruser(self):
        # 非公開カードは作者以外のユーザとして認証されている状態でアクセスした場合は取得できない
        card = Card.objects.get(word='card_rdpuapiview2')
        user = User.objects.get(username='card_rdpuapiview')
        client = APIClient()
        client.force_login(user)

        response = client.get(reverse('api:v1:cards:detail',
                                      kwargs={'id': card.id}))

        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 403)

    def test_6_success_update(self):
        # そのカードのauthorとしてログインしている場合は適切な入力値でカードのword,answer
        # is_hiddenを更新する事が出来る
        user = User.objects.get(username='card_rdpuapiview')
        client = APIClient()
        client.force_login(user)
        params = {
            'word': 'updated_card_rdpuapiview',
            'answer': 'updated_card_rdpuapiview',
            'is_hidden': True,
        }

        card = Card.objects.get(word='card_rdpuapiview')
        response = client.patch(reverse('api:v1:cards:detail',
                                        kwargs={'id': card.id}),
                                params,
                                format='json')

        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 200)
        # カードが更新されたか検証
        updated_card = Card.objects.get(id=card.id)
        self.assertEqual(updated_card.word, 'updated_card_rdpuapiview')
        self.assertEqual(updated_card.answer, 'updated_card_rdpuapiview')

    def test_7_fail_update_unauthorization(self):
        # 認証されていない場合は適切な入力値でもカードのword,answer,is_hiddenを
        # 更新する事が出来ない (403が返ってくる)
        client = APIClient()
        params = {
            'word': 'updated_card_rdpuapiview',
            'answer': 'updated_card_rdpuapiview',
            'is_hidden': True,
        }

        card = Card.objects.get(word='card_rdpuapiview')
        response = client.patch(reverse('api:v1:cards:detail',
                                        kwargs={'id': card.id}),
                                params,
                                format='json')

        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 403)

    def test_8_fail_update_other_user(self):
        # author以外のユーザとして認証されている場合は適切な入力値でもカードのwordとanswer
        # #を更新する事が出来ない (403が返ってくる)
        user = User.objects.get(username='card_rdpuapiview2')
        client = APIClient()
        client.force_login(user)
        params = {
            'word': 'updated_card_rdpuapiview',
            'answer': 'updated_card_rdpuapiview',
            'is_hidden': True,
        }

        card = Card.objects.get(word='card_rdpuapiview')
        response = client.patch(reverse('api:v1:cards:detail',
                                        kwargs={'id': card.id}),
                                params,
                                format='json')

        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 403)

    def test_9_fail_update_wrong_params(self):
        # そのカードのauthorとしてログインしている場合でも不適切な入力値では
        # カードのwordとanswerを更新する事が出来ない (400が返ってくる)
        user = User.objects.get(username='card_rdpuapiview')
        client = APIClient()
        client.force_login(user)

        wrong_params_list = [
            {
                'word': '',
                'answer': 'updated_card_rdpuapiview',
                'is_hidden': True,
            },
            {
                'word': 'updated_card_rdpuapiview',
                'answer': '',
                'is_hidden': True,
            },
            {
                'word': 'A' * 101,
                'answer': 'updated_card_rdpuapiview',
                'is_hidden': True,
            },
            {
                'word': 'updated_card_rdpuapiview',
                'answer': 'A' * 201,
                'is_hidden': True,
            },
            {
                'word': 'updated_card_rdpuapiview',
                'answer': 'updated_card_rdpuapiview',
                'is_hidden': 'wrong_param',
            },
        ]

        card = Card.objects.get(word='card_rdpuapiview')

        for wrong_params in wrong_params_list:
            response = client.patch(reverse('api:v1:cards:detail',
                                            kwargs={'id': card.id}),
                                    wrong_params,
                                    format='json')
            # HTTPステータスコードの検証
            self.assertEqual(response.status_code, 400)

    def test_10_success_delete(self):
        # そのカードのauthorとしてログインしている場合はそのカードを削除できる
        # (204が返ってくる)
        user = User.objects.get(username='card_rdpuapiview')
        client = APIClient()
        client.force_login(user)

        card = Card.objects.get(word='card_rdpuapiview')
        response = client.delete(reverse('api:v1:cards:detail',
                                         kwargs={'id': card.id}))

        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 204)
        # カードが削除されたか検証
        with self.assertRaises(ObjectDoesNotExist):
            card = Card.objects.get(word='card_rdpuapiview')

    def test_11_fail_update_unauthorization(self):
        # 認証されていない場合はそのカードを削除する事は出来ない
        client = APIClient()
        card = Card.objects.get(word='card_rdpuapiview')
        response = client.delete(reverse('api:v1:cards:detail',
                                         kwargs={'id': card.id}))

        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 403)

    def test_12_fail_update_other_user(self):
        # author以外のユーザとして認証されている場合はそのカードを削除する事は出来ない
        user = User.objects.get(username='card_rdpuapiview2')
        client = APIClient()
        client.force_login(user)

        card = Card.objects.get(word='card_rdpuapiview')
        response = client.delete(reverse('api:v1:cards:detail',
                                         kwargs={'id': card.id}))

        # HTTPレスポンスステータスコードの検証
        self.assertEqual(response.status_code, 403)
