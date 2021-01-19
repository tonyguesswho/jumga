from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin

from django.utils.translation import gettext_lazy as _

from apps.delivery.models import Rider
# from apps.seller.models import Seller
# from apps.user.models import User

import uuid


class AbstractTimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and save a new user"""
        if not email:
            raise ValueError('Email is required')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and save super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin, AbstractTimeStampedModel):
    """Custom user model """
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Account(models.Model):

    user = models.OneToOneField(
        User, related_name='seller_account', on_delete=models.CASCADE, null=True, blank=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    country_code = models.CharField(_('alpha 2 country code'), max_length=3)

    account_number = models.CharField(_('acc'), max_length=50,  null=True)

    bank = models.CharField(_('bank'), max_length=50,  null=True)

    subaccount_id = models.CharField(_('account_id'), max_length=100)

    currency = models.CharField(_('currency'), max_length=3, default='USD')

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
