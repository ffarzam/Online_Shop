from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('login/refresh/', views.RefreshToken.as_view(), name='token_refresh'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('logout_all/', views.LogoutAll.as_view(), name='logout_all'),
    path('active_login/', views.CheckAllActiveLogin.as_view(), name='active_login'),
    path('selected_logout/', views.SelectedLogout.as_view(), name='selected_logout'),
    path('profile/', views.ShowProfile.as_view(), name='profile'),
    path('change_password/<int:pk>', views.ChangePasswordView.as_view(), name='change_password'),
    path('update_profile/<int:pk>', views.UpdateProfileView.as_view(), name='update_profile'),
    path('create_address/', views.CreateAddress.as_view(), name='create_address'),
    path('update_address/<int:pk>', views.UpdateAddress.as_view(), name='update_address'),
    path('remove_address/<int:pk>', views.RemoveAddress.as_view(), name='remove_address'),
    path('get_address/<int:pk>', views.GetAddress.as_view(), name='get_address'),
    path('address_list/', views.AddressList.as_view(), name='address_list'),
]


