import json

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from http.cookies import SimpleCookie

from accounts.models import CustomUser


class TestRegister(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")

    def tearDown(self):
        CustomUser.objects.all().delete()

    def test_success_register(self):
        user_data = {
            "username": "ffarzam",
            "email": "ffarzam_1992@yahoo.com",
            "password": "ffarzam_1992",
            "password2": "ffarzam_1992"
        }

        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, 201)

    def test_fail_register_short_username(self):
        user_data = {
            "username": "Ali",
            "email": "ali@yahoo.com",
            "password": "ali_1992",
            "password2": "ali_1992"
        }

        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["username"][0], "Username must be more than 6 characters long")

    def test_fail_register_long_username(self):
        user_data = {
            "username": "this is a long username for test",
            "email": "ali@yahoo.com",
            "password": "ali_1992",
            "password2": "ali_1992"
        }

        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["username"][0], "Ensure this field has no more than 25 characters.")

    def test_fail_register_same_username_and_email(self):
        user_data = {
            "username": "ali@yahoo.com",
            "email": "ali@yahoo.com",
            "password": "ali_1992",
            "password2": "ali_1992"
        }

        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["non_field_errors"][0], "Email and username can't be same")

    def test_fail_register_same_username_and_password(self):
        user_data = {
            "username": "ali_1992",
            "email": "ali@yahoo.com",
            "password": "ali_1992",
            "password2": "ali_1992"
        }

        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["non_field_errors"][0], "Password and username can't be same")

    def test_fail_register_password_not_match(self):
        user_data = {
            "username": "ali1992",
            "email": "ali@yahoo.com",
            "password": "ali_1992",
            "password2": "ali_1991"
        }

        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["non_field_errors"][0], "Passwords don't match")

    def test_fail_register_not_unique_username(self):
        user1_data = {
            "username": "ali1992",
            "email": "ali@yahoo.com",
            "password": "ali_1992",
            "password2": "ali_1992"
        }
        self.client.post(self.register_url, user1_data)

        user2_data = {
            "username": "ali1992",
            "email": "ali2@yahoo.com",
            "password": "ali2_1992",
            "password2": "ali2_1992"
        }

        response = self.client.post(self.register_url, user2_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["username"][0], "custom user with this Username already exists.")

    def test_fail_register_not_unique_email(self):
        user1_data = {
            "username": "ali1992",
            "email": "ali@yahoo.com",
            "password": "ali_1992",
            "password2": "ali_1992"
        }
        self.client.post(self.register_url, user1_data)

        user2_data = {
            "username": "ali21992",
            "email": "ali@yahoo.com",
            "password": "ali2_1992",
            "password2": "ali2_1992"
        }

        response = self.client.post(self.register_url, user2_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["email"][0], "custom user with this Email already exists.")

    def test_fail_register_short_password(self):
        user_data = {
            "username": "ali1992",
            "email": "ali@yahoo.com",
            "password": "ali",
            "password2": "ali"
        }

        response = self.client.post(self.register_url, user_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["password"][0],
                         "This password is too short. It must contain at least 8 characters.")


class TestLogin(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("login")

        user_data = {
            "username": "ffarzam",
            "email": "ffarzam_1992@yahoo.com",
            "password": "ffarzam_1992",
        }
        CustomUser.objects.create_user(**user_data)

    def tearDown(self):
        CustomUser.objects.all().delete()

    def test_successful_login(self):
        login_data = {
            "user_identifier": "ffarzam",
            "password": "ffarzam_1992",
        }

        response = self.client.post(self.login_url, login_data, HTTP_USER_AGENT='Mozilla/5.0', USERNAME='ffarzam')
        self.assertEqual(response.status_code, 201)

    def test_successful_login_with_cookie(self):
        login_data = {
            "user_identifier": "ffarzam",
            "password": "ffarzam_1992",
        }
        self.client.cookies = SimpleCookie({'cart': json.dumps({'1': '5'})})

        response = self.client.post(self.login_url, login_data, HTTP_USER_AGENT='Mozilla/5.0', USERNAME='ffarzam')
        self.assertEqual(response.status_code, 201)

    def test_unsuccessful_login(self):
        login_data = {
            "user_identifier": "farzam",
            "password": "ffarzam_1992",
        }

        response = self.client.post(self.login_url, login_data, HTTP_USER_AGENT='Mozilla/5.0', USERNAME='ffarzam')
        self.assertEqual(response.status_code, 400)
