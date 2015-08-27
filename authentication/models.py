#!/usr/bin/env python
""" Basic Model for Busniness Users"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from localflavor.us.us_states import US_STATES
from localflavor.us import models as usmodels
__author__ = "Chia-Yuan Chuang"
__copyright__ = "Copyright 2015, The Feel Free Project"
__credits__ = ["Chia-Yuan Chuang"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Chia-Yuan Chuang"
__email__ = "lancy0511@gmail.com"
__status__ = "Development"


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        # if not kwargs.get('username'):
        #     raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email),
            businessname=kwargs.get('businessname'),
            zipcode=kwargs.get('zipcode'),
            city=kwargs.get('city'),
            state=kwargs.get('state'),
            phone=kwargs.get('phone'),
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)
        account.is_staff = True
        account.is_admin = True
        account.is_superuser = True
        account.is_active = True
        account.save()

        return account


class Account(AbstractBaseUser):
    """Returns a new Account object inherited from AbstractBaseUser.

    AbstractBaseUser: The parent class of users

    Note: email, businessname, zipcode, city, state, phone
          are required
    """

    email = models.EmailField(max_length=255, unique=True)
    businessname = models.CharField(max_length=35, blank=False,
                                    default='buname')
    spaceId = models.CharField(max_length=10, unique=True,
                               blank=True, null=True)
    zipcode = usmodels.USZipCodeField(blank=False, default='00000')
    city = models.CharField(max_length=50, blank=False,
                            default='--------')
    state = usmodels.USStateField(choices=US_STATES, blank=False,
                                  default='--------')
    phone = usmodels.PhoneNumberField(blank=False, default='000-000-0000')

    SHIRT_SIZES = (
        ('1', 'Silver'),
        ('2', 'Gold'),
        ('3', 'Platinum'),
    )
    tierlist = models.CharField(blank=True, null=True,
                                max_length=1, choices=SHIRT_SIZES)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['businessname', 'zipcode', 'city', 'state', 'phone']

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.email, self.businessname])

    def get_short_name(self):
        return self.email

    def has_module_perms(self, app_label):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin
