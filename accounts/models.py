from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models
from .manager import CustomManager
from .utils import phoneNumberRegex


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=25, verbose_name=_("Username"), unique=True)
    email = models.EmailField(verbose_name=_("Email"), unique=True)
    phone = models.CharField(verbose_name=_("Phone Number"), validators=[phoneNumberRegex], unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name=_("Joined Date"), auto_now_add=True, editable=False)
    last_modify = models.DateTimeField(verbose_name=_("Last Modify"), auto_now=True, editable=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ["email"]

    objects = CustomManager()

    def __str__(self):
        return self.username


class Address(models.Model):
    title = models.CharField(max_length=25)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    alley = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    unit = models.PositiveIntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

