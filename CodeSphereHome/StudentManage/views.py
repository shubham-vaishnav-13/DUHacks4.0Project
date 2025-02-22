from django.shortcuts import render
from .models import CodeFile
# Create your views here.

def home(request):
    return render(request,'StudentManage/home.html',{'files':CodeFile.objects.all()})

