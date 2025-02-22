from django.urls import path
from .views import file_list, upload_file

app_name = "files"

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('files/', file_list, name='file_list'), 
]
