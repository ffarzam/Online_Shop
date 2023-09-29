from django.test import TestCase
from accounts.models import CustomUser, Address
from model_bakery import baker


class TestCustomUser(TestCase):

    def test_str(self):
        user = CustomUser.objects.create_user(username='ffarzam', password='ffarzam', email="ffarzam_1992@yahoo.com")
        self.assertEqual(str(user), 'ffarzam')


class TestAddress(TestCase):

    def test_str(self):
        user = CustomUser.objects.create_user(username='ffarzam', password='ffarzam', email="ffarzam_1992@yahoo.com")

        address = baker.make(Address, title="home", user=user)

        self.assertEqual(str(address), f"ffarzam || home")
