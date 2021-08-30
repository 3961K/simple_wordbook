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

        for i in range(1, 6):
            Card.objects.create(
                word='wordbook_serializer_{}'.format(i),
                answer='wordbook_serializer_{}'.format(i),
                author=user
            )

        Wordbook.objects.create(
            wordbook_name='wordbook_serializer',
            author=user
        )

    def test_1_valid_and_success_add_cards(self):
        # 適切な入力値は妥当であり,単語帳にカードを追加する事が出来る
        card = Card.objects.get(word='wordbook_serializer_1')
        card2 = Card.objects.get(word='wordbook_serializer_2')

        params = {
            'wordbook_name': 'updated_wordbook_serializer',
            'is_hidden': True,
            'add_cards': [
                card.id,
                card2.id,
            ],
            'delete_cards': [
            ]
        }

        wordbook = Wordbook.objects.get(wordbook_name='wordbook_serializer')
        # バリデーション結果の検証
        serializer = WordbookUpdateSerializer(instance=wordbook, data=params)
        self.assertTrue(serializer.is_valid())
        # 単語帳にカードが追加されたか検証
        serializer.save()
        added_wordbook = Wordbook.objects.get(wordbook_name='updated_wordbook_serializer')
        self.assertEqual(len(added_wordbook.cards.all()), 2)

    def test_2_valid_and_success_delete_cards(self):
        # 適切な入力値は妥当であり,単語帳からカードを削除する事が出来る
        card = Card.objects.get(word='wordbook_serializer_1')
        card2 = Card.objects.get(word='wordbook_serializer_2')

        wordbook = Wordbook.objects.get(wordbook_name='wordbook_serializer')
        wordbook.cards.add(card)
        wordbook.cards.add(card2)

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
        serializer = WordbookUpdateSerializer(instance=wordbook, data=params)
        self.assertTrue(serializer.is_valid())
        # 単語帳からカードが削除されたか検証
        serializer.save()
        added_wordbook = Wordbook.objects.get(wordbook_name='updated_wordbook_serializer')
        self.assertEqual(len(added_wordbook.cards.all()), 0)

    def test_3_invalid(self):
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
            serializer = WordbookUpdateSerializer(instance=wordbook, data=wrong_params)
            self.assertFalse(serializer.is_valid())
