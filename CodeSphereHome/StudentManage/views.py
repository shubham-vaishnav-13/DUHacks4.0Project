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
    search_term = request.GET.get('search')
    files = CodeFile.objects.all()

    if search_term:
        files = files.filter(file_name__icontains=search_term)

    return render(request, 'StudentManage/home.html', {'files': files, 'student': request.user, 'search_term': search_term})

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
    try:
        with open(file_path, 'r', encoding='utf-8') as f:  # Specify encoding here
            file_content = f.read()
        return render(request, 'StudentManage/view_file.html', {'file_obj': file_obj, 'file_content': file_content})
    except FileNotFoundError:
        raise Http404("File not found")

def editor(request, file_id):
    file_obj = get_object_or_404(CodeFile, id=file_id)
    