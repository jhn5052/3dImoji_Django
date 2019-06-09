from django.contrib import admin

# Register your models here.

from .models import UploadFileModel


admin.site.register(UploadFileModel)