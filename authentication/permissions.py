#!/usr/bin/env python
""" Account Permissions for Feel Free Site"""
from rest_framework import permissions
__author__ = "Chia-Yuan Chuang"
__copyright__ = "Copyright 2015, The Feel Free Project"
__credits__ = ["Chia-Yuan Chuang"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Chia-Yuan Chuang"
__email__ = "lancy0511@gmail.com"
__status__ = "Development"


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, account):
        if request.user:
            return account == request.user
        return False
