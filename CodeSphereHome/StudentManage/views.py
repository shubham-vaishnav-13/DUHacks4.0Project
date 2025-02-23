from django.shortcuts import render,redirect
from .models import CodeFile
from django.http import FileResponse
# Create your views here.

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
    response = FileResponse(file.file)
    response['Content-Disposition'] = f'attachment; filename="{file.file_name}"'
    return response

