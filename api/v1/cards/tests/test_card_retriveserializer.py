from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from ..models import Card
from ..serializers import CardRetrieveSerializer

User = get_user_model()


class CardRetrieveSerializerTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create(
            username='card_retrieve_serializer',
            email='card_retrieve_serializer@test.com',
            password='testpassw0rd123',
        )
        user.save()

        Card.objects.create(
            word='card_retrieve_serializer',
            answer='card_retrieve_serializer',
            author=user
        )

    def test_1_success_retrive(self):
        # シリアライザを介して指定したカードオブジェクトを取得する事が出来る
        card = Card.objects.get(word='card_retrieve_serializer')
        serializer = CardRetrieveSerializer(instance=card)
        # 取得したデータの内容を比較する (項目名によって検査する)
        expected_fields = ['word', 'answer', 'is_hidden', 'id', 'create_date']
        for expected_field, serializer_field in zip(expected_fields, serializer.data.keys()):
            self.assertEqual(expected_field, serializer_field)
