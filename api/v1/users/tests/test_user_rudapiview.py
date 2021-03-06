from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from io import BytesIO
from PIL import Image
from rest_framework.test import APITestCase, APIClient
from shutil import rmtree
from tempfile import mkdtemp

User = get_user_model()


class UserRetrieveUpdateDestroyAPIViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = mkdtemp()
        User.objects.create_user(username='user_rudapiview',
                                 email='user_rudapiview@test.com',
                                 password='testpassw0rd123')

        User.objects.create_user(username='user_rudapiviewA',
                                 email='user_rudapiviewA@test.com',
                                 password='testpassw0rd123')

        User.objects.create_user(username='user_rudapiview_super',
                                 email='user_rudapiview_super@test.com',
                                 is_superuser=True,
                                 password='testpassw0rd123')

        User.objects.create_user(username='user_rudapiview_staff',
                                 email='user_rudapiview_staff@test.com',
                                 is_staff=True,
                                 password='testpassw0rd123')

    def test_1_success_access_and_retrive(self):
        # APIViewに対してアクセスする事と指定したユーザの情報を取得する事が出来る
        client = APIClient()
        response = client.get(reverse('api:v1:users:detail',
                                      kwargs={'username': 'user_rudapiview'}))

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)
        # JSONレスポンスの確認
        expected_json = {"username": "user_rudapiview",
                         "icon": "http://testserver/media/images/default.png"}
        self.assertJSONEqual(response.content, expected_json)

    def test_2_fail_access_not_exist(self):
        # 存在しないユーザ名を指定してAPIViewに対してアクセスすると404が返される
        client = APIClient()
        response = client.get(reverse('api:v1:users:detail',
                                      kwargs={'username': 'fail_access'}))

        # ステータスコードの確認
        self.assertEqual(response.status_code, 404)
        # JSONレスポンスの確認
        expected_json = {"detail": "見つかりませんでした。"}
        self.assertJSONEqual(response.content, expected_json)

    def test_3_fail_access_superuser_or_staffuser(self):
        # superuser権限またはstaff権限を持つユーザの詳細情報を取得する事は出来ない
        client = APIClient()

        # ステータスコードの確認 (superuser権限を持つユーザ)
        response = client.get(reverse('api:v1:users:detail',
                                      kwargs={'username': 'user_rudapiview_super'}))

        self.assertEqual(response.status_code, 404)

        # ステータスコードの確認 (staff権限を持つユーザ)
        response = client.get(reverse('api:v1:users:detail',
                                      kwargs={'username': 'user_rudapiview_staff'}))

        self.assertEqual(response.status_code, 404)

    def test_4_success_update(self):
        # APIViewに対して適切な入力値を送信する事によってユーザ情報を更新する事が出来る
        # 現状Webページでのみ利用するので,フォームを利用したユニットテストを作成した
        img_file = BytesIO()
        img = Image.new('RGBA', size=(512, 512), color=(255, 255, 255))
        img.save(img_file, 'png')
        img_file.name = 'test.png'
        img_file.seek(0)

        img_dict = {
            'icon': SimpleUploadedFile(
                img_file.name,
                img_file.read(),
                content_type='image/png')}
        params = {
            'username': 'user_rudapiview2',
            'email': 'user_rudapiview2@test.com',
            'icon': img_dict['icon']
        }

        user = User.objects.get(username='user_rudapiview')
        user_id = user.id
        self.client.force_login(user)
        response = self.client.patch(reverse('api:v1:users:detail',
                                             kwargs={'username': 'user_rudapiview'}),
                                     params,
                                     format='multipart')
        # HTTPレスポンスステータスコードの確認
        self.assertEqual(response.status_code, 200)
        # 情報が更新されたか確認
        updated_user = User.objects.get(id=user_id)
        self.assertEqual(updated_user.username, 'user_rudapiview2')
        self.assertEqual(updated_user.email, 'user_rudapiview2@test.com')
        self.assertEqual(updated_user.icon, 'images/test.png')

    def test_5_success_delete(self):
        # APIViewに対してログインしているユーザと同じユーザ名のユーザを削除する事が出来る
        user = User.objects.get(username='user_rudapiview')
        client = APIClient()
        client.force_login(user)
        response = client.delete(reverse('api:v1:users:detail',
                                         kwargs={'username': 'user_rudapiview'}))
        self.assertEqual(response.status_code, 204)

    @classmethod
    def tearDownClass(cls):
        # テストで作成した画像ファイルを格納しているディレクトリを削除する
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
