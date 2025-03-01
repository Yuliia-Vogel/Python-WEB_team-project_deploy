import os
import logging
import requests
from django.http import JsonResponse
import cloudinary.uploader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadFileForm
from .models import UploadedFile

CATEGORY_MAP = {
    "images": ["jpg", "jpeg", "png", "gif", "webp", "svg"],
    "documents": ["pdf", "doc", "docx", "xls", "xlsx", "txt", "ppt", "pptx"],
    "videos": ["mp4", "avi", "mov", "mkv", "flv", "wmv"],
    "audio": ["mp3", "wav", "ogg", "flac", "aac", "m4a"],
    "archives": ["zip", "rar", "7z", "tar", "gz"],
}

FORBIDDEN_EXTENSIONS = ['.exe']

logger = logging.getLogger(__name__)

def get_file_category(filename):
    ext = filename.split(".")[-1].lower()
    for category, extensions in CATEGORY_MAP.items():
        if ext in extensions:
            return category
    return "other"



@login_required
def upload_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({"error": "File is required"}, status=400)

        uploaded_file = request.FILES['file']
        
        # Перевірка на порожній файл
        if uploaded_file.size == 0:
            form = UploadFileForm()  # Повторно ініціалізуємо форму, щоб не було помилки при рендерингу
            return render(request, 'assistant_app/upload_file.html', {
                'form': form,
                'error': "The file is empty."  # Передаємо повідомлення про помилку
            })
        
        # Перевірка на заборонене розширення
        file_name, file_extension = os.path.splitext(uploaded_file.name)
        if file_extension.lower() in FORBIDDEN_EXTENSIONS:
            form = UploadFileForm()  # Повторно ініціалізуємо форму
            return render(request, 'assistant_app/upload_file.html', {
                'form': form,
                'error': "Exe files are not allowed to upload."  # Повідомлення про заборонений файл
            })

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            category = get_file_category(uploaded_file.name)
            folder_name = f"users_files/{request.user.email}/{category}"
            uploaded_data = cloudinary.uploader.upload(
                uploaded_file,
                folder=folder_name,
                resource_type='auto',
                public_id=uploaded_file.name
            )
            logger.info(f"Uploading: {uploaded_file.name}")
            UploadedFile.objects.create(user=request.user, 
                                        file_url=uploaded_data["secure_url"],
                                        public_id=uploaded_data["public_id"])

            return render(request, 'assistant_app/upload_success.html', {
                'file_name': uploaded_file.name,
                'file_url': uploaded_data["secure_url"]
            })

    else:
        form = UploadFileForm()
    return render(request, 'assistant_app/upload_file.html', {'form': form})


@login_required
def file_list(request):
    files = UploadedFile.objects.filter(user=request.user)  # Фільтруємо файли поточного юзера
    category = request.GET.get("category", "all")  # Отримуємо категорію з GET-запиту

    valid_files = []

    for file in files:
        try:
            response = requests.head(file.file_url, timeout=5)  # Перевіряємо чи файл існує
            if response.status_code == 200:
                # Отримуємо назву папки з URL файлу
                folder_name = file.file_url.split("/")[-2]  # передостанній елемент - це папка

                # Фільтруємо за категорією
                if category == "all" or folder_name == category:
                    valid_files.append(file)
        except requests.RequestException:
            pass  # Файл не знайдено або інша помилка

    return render(request, "assistant_app/file_list.html", {
        "files": valid_files,
        "selected_category": category
    })


@login_required
def download_file(request, file_id):
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
    

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id, user=request.user)

    logger.info(f"Deleting: {file.public_id}")
    # Видаляємо файл із клаудінері
    # cloudinary.uploader.destroy(file.public_id)

    # gросто видаляємо об'єкт, і `delete()` сам подбає про Cloudinary (бо ми перевизначили функцію видалення в класі UploadedFile)
    file.delete()

    return render(request, 'assistant_app/file_deleted.html')


