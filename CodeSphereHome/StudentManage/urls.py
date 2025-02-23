from django.urls import path,include

from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('upload/',views.upload_file,name='upload_file'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
]
