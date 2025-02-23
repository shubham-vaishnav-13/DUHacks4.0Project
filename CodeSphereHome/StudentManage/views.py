from django.shortcuts import render,redirect
from .models import CodeFile
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from urllib.parse import quote

# Create your views here.

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

from django.shortcuts import redirect, get_object_or_404

def delete_file(request, file_id):
    if request.method == 'POST':
        file = get_object_or_404(CodeFile, id=file_id)
        file.delete()
        return redirect('home')  # Redirect to the home page or another appropriate page
    return redirect('home')  # Redirect if not a POST request


def download_file(request, file_id):
    file = get_object_or_404(CodeFile, id=file_id)
    file_path = file.file.path
    file_name = file.file_name  # Use the stored file name

    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/force-download")
            response['Content-Disposition'] = f'attachment; filename="{quote(file_name)}"'  # Properly encode the filename
            return response
    except FileNotFoundError:
        raise Http404("File not found")


def view_file(request, file_id):
    file_obj = get_object_or_404(CodeFile, id=file_id)
    file_path = file_obj.file.path
    file_name = os.path.basename(file_path)
    try:
        with open(file_path, 'r') as f:
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
    