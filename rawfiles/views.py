from django.shortcuts import render , redirect
import os
from django.conf import settings
from django.http import HttpResponse
from .models import RawFiles , RawFaces
import uuid
import cv2
import json

def savecutting(request):
    raw_data = request.body
    #print(raw_data)
    try:
        json_data = json.loads(raw_data)
        #print(json_data['original'])
        #print(json_data['deleteImages'])
        delList = []
        for delimg in json_data['deleteImages']:
            delList.append(delimg['fname'])

        for key in json_data['original'].keys():
            obj = json_data['original'].get(key)
            faceList = obj.get('faces')
            for dl in delList:
                if dl in faceList:
                    i = faceList.index(dl)
                    faceList.pop(i)
                    flpath = "appfiles/faces/"+dl
                    os.remove(flpath)
        print(json_data['original'])
        for key in json_data['original'].keys():
            obj = json_data['original'].get(key)
            rawObj = RawFiles.objects.get(pk=key)
            faceList = obj.get('faces')
            for fc in faceList:
                ob = RawFaces()
                ob.image = fc
                ob.rawfile = rawObj
                ob.save()  
            rawObj.isFaceCut = True 
            rawObj.save() 
        return HttpResponse(json.dumps({'msg':'Face Cutting Done !'}))
    except Exception as ex:
        print(ex)
def startcutter(request):
    records = RawFiles.objects.filter(isFaceCut=False)
    facesRecords = dict()
    # Load the cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    for rec in records:
        # Read the input image
        image_path = 'appfiles/rawfiles/'+rec.image
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))
        imgList = []
        for (x, y, w, h) in faces:
            # Extract the face region
            face = img[y:y+h, x:x+w]            
            # Optionally, save the extracted face
            fname = str(uuid.uuid4()) + ".jpg"
            face_output_path = 'appfiles/faces/'+ fname
            cv2.imwrite(face_output_path, face)
            imgList.append(fname)
        rec.isFaceCut=True
        rec.save() 
        facesRecords[rec.id] = {'id':rec.id,'real': rec.image , 'faces' : imgList}
    #all_files = os.listdir('appfiles/faces/')       
    return HttpResponse(json.dumps(facesRecords))

def savepic(request):
    if request.method == 'POST' and request.FILES['file']: 
        files = request.FILES.getlist('file')
        for uploaded_file in files:
            fileName = str(uuid.uuid4())+uploaded_file.name[uploaded_file.name.rfind('.'):]

            save_path = os.path.join(settings.MEDIA_ROOT, fileName)
            
            with open(save_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            ob = RawFiles()
            ob.image = fileName
            ob.save()

        return redirect("/uploads")
    
    return redirect("/uploads")
