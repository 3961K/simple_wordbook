from django.contrib.auth import get_user_model
from json import dumps as json_dump
from rest_framework.test import APITestCase

from ..serializers import UserSerializer

User = get_user_model()


class UserSerializerTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for i in range(1, 6):
            User.objects.create_user(
                username='user_serializer_{}'.format(i),
                email='user_serializer_{}@test.com'.format(i),
                password='testpassw0rd123',
                icon='iamges/user_serializer_{}.png'.format(i))

    def test_success_get_list(self):
        users = User.objects.all()
        serializer = UserSerializer(instance=users, many=True)
        # 予想したJSON形式の文字列をシリアライザから取得できる
        expected_json_str = '[{"username": "user_serializer_1", "icon": "/media/iamges/user_serializer_1.png"}, {"username": "user_serializer_2", "icon": "/media/iamges/user_serializer_2.png"}, {"username": "user_serializer_3", "icon": "/media/iamges/user_serializer_3.png"}, {"username": "user_serializer_4", "icon": "/media/iamges/user_serializer_4.png"}, {"username": "user_serializer_5", "icon": "/media/iamges/user_serializer_5.png"}]'
        self.assertEqual(expected_json_str, json_dump(serializer.data))
