import datetime
import os
import random
import string
from datetime import datetime

import requests
from boto3 import Session
from django.conf import settings
from django.conf.global_settings import MEDIA_ROOT

from market_backend.apps.accounts.models import Media
from market_backend.v0.accounts import serializers


class AccountsUtils:
    """
    Utility methods related to Accounts Application
    """

    @staticmethod
    def get_user_full_name(user):
        if isinstance(user, list):
            user_name_list = ''
            for i, _ in enumerate(user):
                if i != 0:
                    user_name_list += ' / '
                if _.first_name or _.last_name:
                    user_name_list += "{} {}".format(_.first_name, _.last_name)
                    user_name_list += "{}".format(_.username.split('@')[0])
            return user_name_list
        if user.first_name or user.last_name:
            return "{} {}".format(user.first_name, user.last_name)
        return "{}".format(user.username.split('@')[0])

    @staticmethod
    def get_readable_user_type(type):
        return type.replace('_', ' ').lower().capitalize()


class FileUploadUtils(object):
    @staticmethod
    def getFileKey():
        return ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(50))

    @staticmethod
    def deleteFile(key):
        media = Media.objects.get(id=key)

        session = Session(aws_access_key_id=settings.AWS_ACCESS_KEY,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_REGION_NAME)
        s3 = session.resource('s3')
        my_bucket = s3.Bucket(settings.AWS_BUCKET_NAME)
        response = my_bucket.delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': media.key
                    }
                ]
            }
        )
        media.delete()
        return response

    @staticmethod
    def getFileName(key):
        try:
            file = Media.objects.get(key=key)
            return file.file_name
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def getContentType(extension, url=None):
        if extension == 'pdf':
            return 'application/pdf'
        elif extension == 'png':
            return 'image/png'
        elif extension == 'jpeg' or extension == 'jpg':
            return 'image/jpeg'
        else:
            return 'image/jpeg'

    @staticmethod
    def uploadFile(url):
        filename = url.split("/")[-1]
        fileextension = filename.split('.')[1]
        file = requests.get(url).content
        filepath = os.path.join(MEDIA_ROOT, filename)
        with open(filepath, 'wb') as destination:
            destination.write(file)
        file = open(filepath, 'rb')
        extension = FileUploadUtils.getContentType(fileextension)
        valid_file = True
        if extension is None:
            valid_file = False
        session = Session(aws_access_key_id=settings.AWS_ACCESS_KEY,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_REGION_NAME)
        s3 = session.resource('s3')
        file_key = FileUploadUtils.getFileKey()
        if valid_file:
            res = s3.Bucket(settings.AWS_BUCKET_NAME).put_object(Key=file_key, Body=file, ContentType=extension,
                                                                 ACL='public-read')
            data = {'key': file_key, 'file_name': filename, 'is_link': True}
            serializer = serializers.CreateFileUploadSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            if os.path.isfile(filepath):
                os.remove(filepath)
            media = Media.objects.get(key=file_key)
            return media
        else:
            return None

    @staticmethod
    def upload_file_by_file(file):
        milli_sec = str(datetime.datetime.now())
        filename = str(milli_sec) + '.pdf'
        print(file)
        session = Session(aws_access_key_id=settings.AWS_ACCESS_KEY,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_REGION_NAME)
        s3 = session.resource('s3')
        file_key = FileUploadUtils.getFileKey()
        res = s3.Bucket(settings.AWS_BUCKET_NAME).put_object(Key=file_key, Body=file, ContentType='application/pdf',
                                                             ACL='public-read')
        data = {'key': file_key, 'file_name': filename, 'is_link': False}
        serializer = serializers.CreateFileUploadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        media = Media.objects.get(key=file_key)
        return media

    @staticmethod
    def get_url_from_media_object(media):
        return settings.AWS_S3_BASE_LINK + media.key
