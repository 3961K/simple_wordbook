from functools import partial
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from ..models import Wordbook
from ...cards.models import Card
from ..serializers import WordbookUpdateSerializer

User = get_user_model()


class WordbookSerializerTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create(
            username='wordbook_serializer',
            email='wordbook_serializer@test.com',
            password='testpassw0rd123',
        )
        user.save()

        user2 = User.objects.create(
            username='wordbook_serializer2',
            email='wordbook_serializer2@test.com',
            password='testpassw0rd123',
        )
        user2.save()

        for i in range(1, 6):
            Card.objects.create(
                word='wordbook_serializer_{}'.format(i),
                answer='wordbook_serializer_{}'.format(i),
                author=user
            )

        Card.objects.create(
            word='wordbook_serializer_hidden',
            answer='wordbook_serializer_hidden',
            is_hidden=True,
            author=user2
        )

        Wordbook.objects.create(
            wordbook_name='wordbook_serializer',
            author=user
        )

    def test_1_valid_and_success_add_cards(self):
        # 適切な入力値は妥当であり,単語帳にカードを追加する事が出来る
        card = Card.objects.get(word='wordbook_serializer_1')
        card2 = Card.objects.get(word='wordbook_serializer_2')
        hidden_card = Card.objects.get(word='wordbook_serializer_hidden')

        params = {
            'wordbook_name': 'updated_wordbook_serializer',
            'is_hidden': True,
            'add_cards': [
                card.id,
                card2.id,
                hidden_card.id,
            ],
            'delete_cards': [
            ]
        }

        wordbook = Wordbook.objects.get(wordbook_name='wordbook_serializer')
        # バリデーション結果の検証
        serializer = WordbookUpdateSerializer(instance=wordbook,
                                              data=params,
                                              partial=True)
        self.assertTrue(serializer.is_valid())
        # 単語帳にカードが追加されたか検証
        serializer.save()
        added_wordbook = Wordbook.objects.get(wordbook_name='updated_wordbook_serializer')
        self.assertEqual(len(added_wordbook.cards.all()), 2)
        # 他のユーザが作成した非公開カードのIDを追加する事は出来ない
        self.assertFalse(hidden_card in added_wordbook.cards.all())

    def test_2_valid_and_success_add_cards_with_userinfo(self):
        # 適切な入力値は妥当であり,単語帳にカードを追加する事が出来る
        # また,非公開カードであってもuserに作者の情報を渡している場合は追加する事が出来る
        card = Card.objects.get(word='wordbook_serializer_1')
        card2 = Card.objects.get(word='wordbook_serializer_2')
        hidden_card = Card.objects.get(word='wordbook_serializer_hidden')

        params = {
            'wordbook_name': 'updated_wordbook_serializer',
            'is_hidden': True,
            'add_cards': [
                card.id,
                card2.id,
                hidden_card.id,
            ],
            'delete_cards': [
            ]
        }

        wordbook = Wordbook.objects.get(wordbook_name='wordbook_serializer')
        # バリデーション結果の検証
        user = User.objects.get(username='wordbook_serializer2')
        serializer = WordbookUpdateSerializer(instance=wordbook,
                                              data=params,
                                              partial=True,
                                              user=user)
        self.assertTrue(serializer.is_valid())
        # 単語帳にカードが追加されたか検証
        serializer.save()
        added_wordbook = Wordbook.objects.get(wordbook_name='updated_wordbook_serializer')
        self.assertEqual(len(added_wordbook.cards.all()), 3)

    def test_3_valid_and_success_delete_cards(self):
        # 適切な入力値は妥当であり,単語帳からカードを削除する事が出来る
        card = Card.objects.get(word='wordbook_serializer_1')
        card2 = Card.objects.get(word='wordbook_serializer_2')

        params = {
            'wordbook_name': 'updated_wordbook_serializer',
            'is_hidden': True,
            'add_cards': [
            ],
            'delete_cards': [
                card.id,
                card2.id,
            ]
        }

        # バリデーション結果の検証
        wordbook = Wordbook.objects.get(wordbook_name='wordbook_serializer')
        serializer = WordbookUpdateSerializer(instance=wordbook,
                                              data=params,
                                              partial=True)
        self.assertTrue(serializer.is_valid())
        # 単語帳からカードが削除されたか検証
        serializer.save()
        added_wordbook = Wordbook.objects.get(wordbook_name='updated_wordbook_serializer')
        self.assertEqual(len(added_wordbook.cards.all()), 0)

    def test_4_invalid(self):
        # 誤った形式の値は妥当ではない
        card = Card.objects.get(word='wordbook_serializer_1')
        wordbook = Wordbook.objects.get(wordbook_name='wordbook_serializer')

        wrong_params_list = [
            {
                'wordbook_name': 'A' * 101,
                'is_hidden': True,
                'add_cards': [
                    card.id
                ],
                'delete_cards': [
                ]
            },
            {
                'wordbook_name': 'updated_wordbook_serializer',
                'is_hidden': True,
                'add_cards': [
                    'wrong_param'
                ],
                'delete_cards': [
                    card.id
                ]
            },
            {
                'wordbook_name': 'updated_wordbook_serializer',
                'is_hidden': True,
                'add_cards': [
                    card.id
                ],
                'delete_cards': [
                    'wrong_param'
                ],
            },
            {
                'wordbook_name': 'updated_wordbook_serializer',
                'is_hidden': 'wrong_params',
                'add_cards': [
                    card.id
                ],
                'delete_cards': [
                ],
            },
        ]

        # バリデーション結果の検証
        for wrong_params in wrong_params_list:
            serializer = WordbookUpdateSerializer(instance=wordbook,
                                                  data=wrong_params,
                                                  partial=True)
            self.assertFalse(serializer.is_valid())
