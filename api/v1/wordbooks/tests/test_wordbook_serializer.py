from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from ..models import Wordbook
from ..serializers import WordbookSerializer

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
            Wordbook.objects.create(
                wordbook_name='wordbook_serializer_{}'.format(i),
                is_hidden=False,
                author=user
            )

    def test_1_success_get_list(self):
        wordbooks = Wordbook.objects.all()
        serializer = WordbookSerializer(instance=wordbooks, many=True)
        # 予想した件数を取得する事が出来る
        self.assertEqual(len(serializer.data), 5)
