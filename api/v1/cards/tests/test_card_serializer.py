from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from ..models import Card
from ..serializers import CardSerializer

User = get_user_model()


class CardSerializerTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create(
            username='card_serializer',
            email='card_serializer@test.com',
            password='testpassw0rd123',
        )
        user.save()
        for i in range(1, 6):
            Card.objects.create(
                word='card_serializer{}'.format(i),
                answer='card_serializer{}'.format(i),
                author=user
            )

    def test_1_success_get_list(self):
        cards = Card.objects.all()
        serializer = CardSerializer(instance=cards, many=True)
        # 予想した件数を取得する事が出来る
        self.assertEqual(len(serializer.data), 5)
        # 予想したフィールドの値を取得する事が出来る
        expected_fields = ['id', 'word', 'answer']
        for expected_field, serializer_field in zip(expected_fields, serializer.data[0].keys()):
            self.assertEqual(expected_field, serializer_field)
