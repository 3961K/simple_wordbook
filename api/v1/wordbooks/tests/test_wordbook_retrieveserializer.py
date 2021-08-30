from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from ..models import Wordbook
from ...cards.models import Card
from ..serializers import WordbookRetrieveSerializer

User = get_user_model()


class WordbookRetrieveTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create(
            username='wordbook_serializer',
            email='wordbook_serializer@test.com',
            password='testpassw0rd123',
        )
        user.save()

        wordbook = Wordbook(
            wordbook_name='wordbook_serializer',
            author=user
        )
        wordbook.save()

        for i in range(1, 6):
            card = Card(
                word='wordbook_serializer_{}'.format(i),
                answer='wordbook_serializer_{}'.format(i),
                author=user
            )
            card.save()
            wordbook.cards.add(card)

    def test_1_success_retrieve(self):
        # シリアライザを介してシリアライズされた指定した単語帳のデータを取得する事が出来る
        wordbook = Wordbook.objects.get(wordbook_name='wordbook_serializer')
        serializer = WordbookRetrieveSerializer(instance=wordbook)
        # 取得したデータの内容を比較する (項目)
        expected_fields = ['id', 'wordbook_name', 'create_date', 'is_hidden',
                           'author_name']
        for expected_field, serializer_field in zip(expected_fields, serializer.data.keys()):
            self.assertEqual(expected_field, serializer_field)
