from django.contrib.auth import get_user_model
from django.test import TestCase
from json import dumps as json_dump

from ..serializers import UserSerializer

User = get_user_model()


class UserSerializerTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for i in range(1, 6):
            User.objects.create_user(
                username='user_serializer_{}'.format(i),
                email='user_serializer_{}@test.com'.format(i),
                password='testpassw0rd123',
                icon='user_serializer_{}.png'.format(i))

    def test_valid(self):
        users = User.objects.all()
        serializer = UserSerializer(instance=users, many=True)
        # 予想したJSON形式の文字列をシリアライザから取得できる
        expected_json_str = '[{"username": "user_serializer_1", "icon": "/user_serializer_1.png"}, {"username": "user_serializer_2", "icon": "/user_serializer_2.png"}, {"username": "user_serializer_3", "icon": "/user_serializer_3.png"}, {"username": "user_serializer_4", "icon": "/user_serializer_4.png"}, {"username": "user_serializer_5", "icon": "/user_serializer_5.png"}]'
        self.assertEqual(expected_json_str, json_dump(serializer.data))
