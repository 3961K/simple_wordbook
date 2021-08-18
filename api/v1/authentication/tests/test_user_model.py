from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase

User = get_user_model()


class UserTest(TestCase):
    def test_success_create_user1(self):
        # 必須フィールドのみでユーザを作成出来る
        User.objects.create_user(username='create_user1',
                                 email='create_user1@test.com',
                                 password='testpassw0rd123')
        user = User.objects.get(username='create_user1')
        self.assertIsNotNone(user)

    def test_success_create_user2(self):
        # 必須フィールド以外のフィールドも指定してユーザを作成出来る
        User.objects.create_user(username='create_user2',
                                 email='create_user2@test.com',
                                 password='testpassw0rd123',
                                 icon='create_user2.png',
                                 )
        user = User.objects.get(username='create_user2')
        self.assertIsNotNone(user)

    def test_fail_create_user(self):
        # 必須フィールドであるユーザ名,メールアドレスのどちらかが欠けている場合はユーザ登録する事が出来ない
        with self.assertRaises(TypeError):
            User.objects.create_user(email='fail_create_user@test.com',
                                     password='testpassw0rd123')

        with self.assertRaises(ValueError):
            User.objects.create_user(username='fail_create_user2',
                                     password='testpassw0rd123')

    def test_fail_create_user2(self):
        # 重複するユーザ名とメールアドレスではユーザ登録する事が出来ない
        User.objects.create_user(username='fail_create_user2',
                                 email='fail_create_user2@test.com',
                                 password='testpassw0rd123')

        def create_fail_duplicated_username():
            # 重複するユーザ名によるユーザ作成を試みる
            try:
                with transaction.atomic():
                    User.objects.create_user(username='fail_create_user2',
                                             email='fail_create_user3@test.com',
                                             password='testpassw0rd123')
            except IntegrityError:
                raise IntegrityError()

        with self.assertRaises(IntegrityError):
            create_fail_duplicated_username()

        def create_fail_duplicated_email():
            # 重複するメールアドレスによるユーザ作成を試みる
            try:
                with transaction.atomic():
                    User.objects.create_user(username='fail_create_user3',
                                             email='fail_create_user2@test.com',
                                             password='testpassw0rd123')
            except IntegrityError:
                raise IntegrityError()

        with self.assertRaises(IntegrityError):
            create_fail_duplicated_email()

    def test_succes_delete_user(self):
        # 指定したユーザを削除する事が出来る
        User.objects.create_user(username='delete_user',
                                 email='delete_user@test.com',
                                 password='testpassw0rd123')
        user = User.objects.get(username='delete_user')
        user.delete()
        with self.assertRaises(ObjectDoesNotExist):
            user = User.objects.get(username='delete_user')

    def test_success_update_user(self):
        # 正しい値でユーザのフィールドを更新する事が出来る
        User.objects.create_user(username='update_user',
                                 email='update_user@test.com',
                                 password='testpassw0rd123')

        user = User.objects.get(username='update_user')
        user.username = 'update_user2'
        user.email = 'update_user2@test.com'
        user.save()

        updated_user = User.objects.get(username='update_user2')
        self.assertEqual(updated_user.username, 'update_user2')
        self.assertEqual(updated_user.email, 'update_user2@test.com')

    def test_fail_update_user(self):
        # 重複が許されていないユーザ名・メールアドレスにおいて既に登録されている情報では更新する事が出来ない
        User.objects.create_user(username='fail_update_user',
                                 email='fail_update_user@test.com',
                                 password='testpassw0rd123')
        User.objects.create_user(username='fail_update_user2',
                                 email='fail_update_user2@test.com',
                                 password='testpassw0rd123')

        user = User.objects.get(username='fail_update_user2')

        def update_duplicated_username():
            user.username = 'fail_update_user'
            try:
                with transaction.atomic():
                    user.save()
            except IntegrityError:
                raise IntegrityError()

        with self.assertRaises(IntegrityError):
            update_duplicated_username()

        def update_duplicated_email():
            user.email = 'fail_update_user@test.com'
            try:
                with transaction.atomic():
                    user.save()
            except IntegrityError:
                raise IntegrityError()

        with self.assertRaises(IntegrityError):
            update_duplicated_email()
