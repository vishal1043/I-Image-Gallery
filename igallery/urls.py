from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home),
    path("uploads",views.uploads),
    path("savepic",views.savepic),
    path("facecutter",views.facecutter),

    path("rawfiles/",include('rawfiles.urls'))
]
