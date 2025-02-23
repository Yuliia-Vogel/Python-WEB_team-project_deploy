import requests

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from .forms import UploadFileForm
from .models import UploadedFile


@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = UploadedFile(user=request.user)
            uploaded_file.save(file=request.FILES['file'])  # Передаємо файл у `save()`
            return redirect('files:file_list')
    else:
        form = UploadFileForm()
    return render(request, 'assistant_app/upload_file.html', {'form': form})


@login_required
def file_list(request):
    files = UploadedFile.objects.filter(user=request.user)  # Фільтруємо тільки файли поточного юзера
    return render(request, 'assistant_app/file_list.html', {'files': files})


@login_required
def download_file(request, file_id):
    # file = UploadedFile.objects.get(id=file_id, user=request.user)
    # file_url = file.file_url
    file = get_object_or_404(UploadedFile, id=file_id)
    file_url = file.file_url

    # Отримуємо файл з Cloudinary
    response = requests.get(file_url, stream=True)
    
    if response.status_code == 200:
        # Відповідь, що дозволяє завантажити файл
        response = HttpResponse(response.content, content_type="application/octet-stream")
        response['Content-Disposition'] = f'attachment; filename="{file_url.split("/")[-1]}"'
        return response
    else:
        return HttpResponse("File not found", status=404)