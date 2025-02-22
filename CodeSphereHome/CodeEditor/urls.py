from django.contrib import admin
from django.urls import path, include
from .views import *;
urlpatterns = [
    path("",view=editor,name="editor"),
    path("run_code/", view=runCode, name="run_code"),
]
