#!/usr/bin/env python
""" Admin for Feel Free Site"""
from django.contrib import admin
from django.forms import ModelForm
from .models import Account
__author__ = "Chia-Yuan Chuang"
__copyright__ = "Copyright 2015, The Feel Free Project"
__credits__ = ["Chia-Yuan Chuang"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Chia-Yuan Chuang"
__email__ = "lancy0511@gmail.com"
__status__ = "Development"


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        readonly_fields = []

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        readonly = (f for f in self.fields.items()
                    if getattr(self.Meta, 'readonly_fields', None) and
                    f[0] in self.Meta.readonly_fields)
        for f in readonly:
            f[1].widget.attrs['readonly'] = True

    def clean_spaceId(self):
        return self.cleaned_data['spaceId'] or None


# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    # exclude = ['last_login']
    form = AccountForm
    fields = (
            'email', 'businessname', 'spaceId', 'created_at', 'last_login',
            'updated_at', 'zipcode', 'city', 'state', 'phone',
            'tierlist', 'is_staff', 'is_admin', 'is_superuser', 'is_active')
    readonly_fields = ['last_login', 'created_at', 'updated_at']
