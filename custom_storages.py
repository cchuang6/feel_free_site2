#!/usr/bin/env python
""" Custom Storage for Amazon S3"""
from django.core.files.storage import get_storage_class
from django.conf import settings
from storages.backends.s3boto import S3BotoStorage
from filebrowser_safe.storage import S3BotoStorageMixin
import logging
logger = logging.getLogger(__name__)
__author__ = "Chia-Yuan Chuang"
__copyright__ = "Copyright 2015, The Feel Free Project"
__credits__ = ["Chia-Yuan Chuang"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Chia-Yuan Chuang"
__email__ = "lancy0511@gmail.com"
__status__ = "Development"


class CachedS3BotoStorage(S3BotoStorage, S3BotoStorageMixin):

    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        non_gzipped_file_content = content.file
        name = super(CachedS3BotoStorage, self).save(name, content)
        content.file = non_gzipped_file_content
        self.local_storage._save(name, content)
        return name


class MediaStorage(S3BotoStorage, S3BotoStorageMixin):
    location = settings.MEDIAFILES_LOCATION


def StaticStorage():
    return CachedS3BotoStorage(location=settings.STATICFILES_LOCATION)
