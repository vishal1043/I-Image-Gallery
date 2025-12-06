from django.shortcuts import render
import os
from django.conf import settings
from django.http import HttpResponse

from rawfiles.models import RawFiles


def home(request):
    return render(request,'home.html')

def uploads(request):
    records = RawFiles.objects.all()
    return render(request,'uploads.html',{
        'records' : records
    })

def facecutter(request):
    if request.method == "GET":
        return render(request,'facecutter.html')

def savepic(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        save_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        return HttpResponse('File uploaded successfully.')
    
    return render(request, 'upload.html')