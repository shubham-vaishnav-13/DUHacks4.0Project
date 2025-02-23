import os
import json
import subprocess
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from urllib.parse import quote
from StaffManage.models import Assignmentfrom .models import CodeFile

@login_required
def home(request):
    return render(request,'StudentManage/home.html',{'files':CodeFile.objects.all(),'student':request.user})

def upload_file(request):
    if request.method == 'POST':
        file_name = request.POST.get('file_name')
        subject = request.POST.get('subject')
        file = request.FILES.get('file')
        CodeFile.objects.create(file_name=file_name, subject=subject, file=file, student=request.user)
    return redirect('home')

def delete_file(request, file_id):
    file = get_object_or_404(CodeFile, id=file_id)
    file.delete()
    return redirect('home')

def download_file(request, file_id):
    file = get_object_or_404(CodeFile, id=file_id)
    file_path = file.file.path
    file_name = file.file_name
    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/force-download")
            response['Content-Disposition'] = f'attachment; filename="{quote(file_name)}"'
            return response
    except FileNotFoundError:
        raise Http404("File not found")

def view_file(request, file_id):
    file_obj = get_object_or_404(CodeFile, id=file_id)
    file_path = file_obj.file.path
    try:
        with open(file_path, 'r', encoding='utf-8') as f:  # Specify encoding here
            file_content = f.read()
            if file_name.lower().endswith(('.txt', '.py', '.c', '.cpp', '.java', '.js', '.html','.css','.go','.rb','.swift','.rs','.dart','.ts','.json')): #Added more file extensions for better theme support
                return render(request, 'StudentManage/view_file.html', {'file': file_obj})
            elif file_name.lower().endswith('.pdf'):
                response = HttpResponse(f.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{quote(file_name)}"'
                return response
            else:
                return render(request, 'StudentManage/view_file.html', {'file': file_obj, 'content': "Preview not available for this file type."})

    except FileNotFoundError:
        raise Http404("File not found")

def editor(request, file_id):
    file_obj = get_object_or_404(CodeFile, id=file_id)
    