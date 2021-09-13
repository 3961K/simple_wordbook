from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
from rest_framework.test import APITestCase
from shutil import rmtree
from tempfile import mkdtemp


from ..serializers import UserPrivateSerializer

User = get_user_model()


class UserSerializerTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # テストで画像を格納するのに利用する一時的なディレクトリの作成
        settings.MEDIA_ROOT = mkdtemp()
        User.objects.create_user(
            username='user_privateserializer',
            email='user_privateserializer@test.com',
            password='testpassw0rd123',)

        User.objects.create_user(
            username='user_privateserializerA',
            email='user_privateserializerA@test.com',
            password='testpassw0rd123',)

    def test_1_success_retrive(self):
        # 期待したユーザのデータを取得する事が出来る
        user = User.objects.get(username='user_privateserializer')
        serializer = UserPrivateSerializer(instance=user)
        expected_json = {'username': 'user_privateserializer',
                         'email': 'user_privateserializer@test.com',
                         'icon': '/media/images/default.png'}
        self.assertEqual(serializer.data, expected_json)

    def test_2_valid_and_success_update(self):
        # 適切な入力値は妥当でありユーザ情報(ユーザ名,メアド,アイコン)を更新する事が出来る
        image = BytesIO()
        Image.new('RGB', (512, 512)).save(image, 'PNG')
        image.seek(0)

        params = {
            'username': 'user_privateserializer2',
            'email': 'user_privateserializer2@test.com',
            'icon': SimpleUploadedFile('user_privateserializer2.png',
                                       image.getvalue())
        }

        user = User.objects.get(username='user_privateserializer')
        serializer = UserPrivateSerializer(instance=user, data=params)

        # バリデーション結果の検証
        self.assertTrue(serializer.is_valid())
        serializer.save()
        # 更新が行われたかの検証
        updated_user = User.objects.get(username='user_privateserializer2')
        self.assertEqual(updated_user.email, 'user_privateserializer2@test.com')
        self.assertEqual(updated_user.icon, 'images/user_privateserializer2.png')

    def test_3_success_update_partial(self):
        # シリアライザを定義する時にpartial=Trueとする事で部分的に更新する事が出来る
        image = BytesIO()
        Image.new('RGB', (512, 512)).save(image, 'PNG')
        image.seek(0)

        param_list = [
            {
                'username': 'user_privateserializer3',
            },
            {
                'email': 'user_privateserializer3@test.com',
            },
            {
                'icon': SimpleUploadedFile('user_privateserializer3.png',
                                           image.getvalue())
            }
        ]

        user = User.objects.get(username='user_privateserializer')
        for param in param_list:
            serializer = UserPrivateSerializer(instance=user,
                                               data=param,
                                               partial=True)
            # バリデーション結果の検証
            self.assertTrue(serializer.is_valid())
            serializer.save()
        # 最終的な結果の比較
        updated_user = User.objects.get(username='user_privateserializer3')
        self.assertEqual(updated_user.email, 'user_privateserializer3@test.com')
        self.assertEqual(updated_user.icon, 'images/user_privateserializer3.png')

    def test_4_invalid(self):
        # 重複した値または適切でない入力値は妥当ではない
        valid_image = BytesIO()
        Image.new('RGB', (512, 512)).save(valid_image, 'PNG')
        valid_image.seek(0)

        invalid_image = BytesIO()
        Image.new('RGB', (512, 513)).save(invalid_image, 'PNG')
        invalid_image.seek(0)

        invalid_image2 = BytesIO()
        Image.new('RGB', (513, 512)).save(invalid_image2, 'PNG')
        invalid_image2.seek(0)

        invalid_params_list = [
            {
                'username': 'user_privateserializerA',
                'email': 'user_privateserializer2@test.com',
                'icon': SimpleUploadedFile('user_privateserializer2.png',
                                           valid_image.getvalue())
            },
            {
                'username': 'user_updateserialize2',
                'email': 'user_privateserializerA@test.com',
                'icon': SimpleUploadedFile('user_privateserializer2.png',
                                           valid_image.getvalue())
            },
            {
                'username': 'user_privateserializer2',
                'email': 'user_privateserializer2@test.com',
                'icon': SimpleUploadedFile('user_privateserializer2.png',
                                           invalid_image.getvalue())
            },
            {
                'username': 'user_privateserializer2',
                'email': 'user_privateserializer2@test.com',
                'icon': SimpleUploadedFile('user_privateserializer2.png',
                                           invalid_image2.getvalue())
            },
        ]

        user = User.objects.get(username='user_privateserializer')
        for invalid_params in invalid_params_list:
            serializer = UserPrivateSerializer(instance=user, data=invalid_params)
            self.assertFalse(serializer.is_valid())

    @classmethod
    def tearDownClass(cls):
        # テストで作成した画像ファイルを格納しているディレクトリを削除する
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
