from django.db import models

class RawFiles(models.Model):
    date = models.DateField(auto_now_add=True, blank=True)
    image = models.TextField()
    isFaceCut = models.BooleanField(default=False)

class RawFaces(models.Model):
    date = models.DateField(auto_now_add=True, blank=True)
    image = models.TextField()
    rawfile = models.ForeignKey(RawFiles,on_delete=models.CASCADE)