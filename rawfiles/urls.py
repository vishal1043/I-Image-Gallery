from django.urls import path 
from . import views

urlpatterns = [
    path("savepic",views.savepic),
    path("startcutting",views.startcutter),
    path("savecutting",views.savecutting)
]