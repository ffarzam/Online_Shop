from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts import views


class TestUrls(SimpleTestCase):
    def test_login(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, views.UserLogin)

    def test_token_refresh(self):
        url = reverse('token_refresh')
        self.assertEqual(resolve(url).func.view_class, views.RefreshToken)

    def test_logout(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, views.LogoutView)

    def test_register(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.view_class, views.UserRegister)

    def test_logout_all(self):
        url = reverse('logout_all')
        self.assertEqual(resolve(url).func.view_class, views.LogoutAll)

    def test_active_login(self):
        url = reverse('active_login')
        self.assertEqual(resolve(url).func.view_class, views.CheckAllActiveLogin)

    def test_selected_logout(self):
        url = reverse('selected_logout')
        self.assertEqual(resolve(url).func.view_class, views.SelectedLogout)

    def test_profile(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func.view_class, views.ShowProfile)

    def test_change_password(self):
        url = reverse('change_password',  args=(1,))
        self.assertEqual(resolve(url).func.view_class, views.ChangePasswordView)

    def test_update_profile(self):
        url = reverse('update_profile',  args=(1,))
        self.assertEqual(resolve(url).func.view_class, views.UpdateProfileView)

    def test_create_address(self):
        url = reverse('create_address')
        self.assertEqual(resolve(url).func.view_class, views.CreateAddress)

    def test_update_address(self):
        url = reverse('update_address',  args=(1,))
        self.assertEqual(resolve(url).func.view_class, views.UpdateAddress)

    def test_remove_address(self):
        url = reverse('remove_address',  args=(1,))
        self.assertEqual(resolve(url).func.view_class, views.RemoveAddress)

    def test_get_address(self):
        url = reverse('get_address',  args=(1,))
        self.assertEqual(resolve(url).func.view_class, views.GetAddress)

    def test_address_list(self):
        url = reverse('address_list')
        self.assertEqual(resolve(url).func.view_class, views.AddressList)

