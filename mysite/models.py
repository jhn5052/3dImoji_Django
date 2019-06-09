from django.db import models
from django.utils import timezone
import os
from uuid import uuid4
from django.conf import settings

def path_and_rename(instance, filename):
    upload_to = 'image'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format("face", "jpg")
    else:
        os.remove(os.path.join(settings.MEDIA_ROOT + '/image', "face.jpg"))
        # set filename as random string
        filename = '{}.{}'.format("face", "jpg")
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class UploadFileModel(models.Model):
    name = models.CharField(default='', max_length=50)
    file = models.ImageField(upload_to=path_and_rename, null=True)