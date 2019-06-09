from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from django.utils.safestring import mark_safe   #channels
import json #channels
from .main import *

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            main()
            return HttpResponseRedirect('uploaded')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def uploaded(request):
    
    return render(request, 'uploaded.html')
