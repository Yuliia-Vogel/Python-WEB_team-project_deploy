# import requests

# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
# from django.shortcuts import render, redirect
# from django.shortcuts import get_object_or_404

# from .forms import UploadFileForm
# from .models import UploadedFile


# CATEGORY_MAP = {
#     "images": ["jpg", "jpeg", "png", "gif", "webp", "svg"],
#     "documents": ["pdf", "doc", "docx", "xls", "xlsx", "txt", "ppt", "pptx"],
#     "videos": ["mp4", "avi", "mov", "mkv", "flv", "wmv"],
#     "audio": ["mp3", "wav", "ogg", "flac", "aac", "m4a"],
#     "archives": ["zip", "rar", "7z", "tar", "gz"],
# }


# def get_file_category(file_url):
#     ext = file_url.split(".")[-1].lower()
#     for category, extensions in CATEGORY_MAP.items():
#         if ext in extensions:
#             return category
#     return "other"


# @login_required
# def upload_file(request):
#     if request.method == 'POST' and request.FILES['file']:
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             uploaded_file = UploadedFile(user=request.user)
#             uploaded_file.save(file=request.FILES['file'])  # Передаємо файл у `save()`
#             return redirect('files:file_list')
#     else:
#         form = UploadFileForm()
#     return render(request, 'assistant_app/upload_file.html', {'form': form})


# # HEAD-запит до кожного файлу - для того, щоб перевіряти наявність файлів у реальному часі \/
# @login_required
# def file_list(request):
#     files = UploadedFile.objects.filter(user=request.user)  # Фільтруємо тільки файли поточного юзера
#     valid_files = []

#     for file in files:
#         try:
#             response = requests.head(file.file_url, timeout=5)  # Швидкий HEAD-запит
#             if response.status_code == 200:
#                 valid_files.append(file)
#         except requests.RequestException:
#             pass  # Файл не знайдено або інша помилка

#     return render(request, "assistant_app/file_list.html", {"files": valid_files})

# @login_required
# def download_file(request, file_id):
#     file = get_object_or_404(UploadedFile, id=file_id)
#     file_url = file.file_url

#     # Отримуємо файл з Cloudinary
#     response = requests.get(file_url, stream=True)
    
#     if response.status_code == 200:
#         # Відповідь, що дозволяє завантажити файл
#         response = HttpResponse(response.content, content_type="application/octet-stream")
#         response['Content-Disposition'] = f'attachment; filename="{file_url.split("/")[-1]}"'
#         return response
#     else:
#         return HttpResponse("File not found", status=404)

# # @login_required
# # def file_list(request):
# #     files = UploadedFile.objects.filter(user=request.user)  # Фільтруємо файли поточного юзера
# #     category = request.GET.get("category", "all")  # Отримуємо категорію з GET-запиту
# #     valid_files = []

# #     for file in files:
# #         try:
# #             response = requests.head(file.file_url, timeout=5)  # Перевірка наявності файлу на хмарі
# #             if response.status_code == 200:
# #                 file.category = get_file_category(file.file_url)  # Додаємо категорію
# #                 valid_files.append(file)
# #         except requests.RequestException:
# #             pass  # Файл не знайдено або інша помилка

# #     # Фільтрація файлів за категорією
# #     if category != "all":
# #         valid_files = [file for file in valid_files if file.category == category]

# #     return render(request, "assistant_app/file_list.html", {
# #         "files": valid_files,
# #         "selected_category": category
# #     })

import requests
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


def get_file_category(filename):
    ext = filename.split(".")[-1].lower()
    for category, extensions in CATEGORY_MAP.items():
        if ext in extensions:
            return category
    return "other"


@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            category = get_file_category(uploaded_file.name)

            # Визначаємо папку на основі email юзера та категорії
            folder_name = f"users_files/{request.user.email}/{category}"

            # Завантаження на Cloudinary
            uploaded_data = cloudinary.uploader.upload(
                uploaded_file,
                folder=folder_name,
                resource_type='auto',
                public_id=uploaded_file.name
            )

            # Збереження URL у БД
            UploadedFile.objects.create(user=request.user, file_url=uploaded_data["secure_url"])

            return redirect('files:file_list')

    else:
        form = UploadFileForm()
    return render(request, 'assistant_app/upload_file.html', {'form': form})


# @login_required
# def file_list(request):
#     files = UploadedFile.objects.filter(user=request.user)
#     category = request.GET.get("category", "all")
#     valid_files = []

#     for file in files:
#         try:
#             response = requests.head(file.file_url, timeout=5)
#             if response.status_code == 200:
#                 file.category = get_file_category(file.file_url)  # Додаємо категорію
#                 valid_files.append(file)
#         except requests.RequestException:
#             pass  

#     if category != "all":
#         valid_files = [file for file in valid_files if file.category == category]

#     return render(request, "assistant_app/file_list.html", {
#         "files": valid_files,
#         "selected_category": category
#     })


# @login_required
# def file_list(request):
#     category = request.GET.get("category", "all")  # Отримуємо вибрану категорію. all тут означає: показати всі файли, якщо фільтр не вибраний
#     user_folder = f"users_files/{request.user.email}/"

#     if category == "all":
#         files = UploadedFile.objects.filter(user=request.user)  # Усі файли юзера
#     else:
#         folder_path = f"{user_folder}{CATEGORY_MAP.get(category, 'other')}"
#         try:
#             # Отримуємо список файлів із Cloudinary по вказаній папці
#             cloudinary_files = cloudinary.api.resources(
#                 type="upload", prefix=folder_path, max_results=100
#             )
#             files = [
#                 UploadedFile(user=request.user, file_url=file["secure_url"])
#                 for file in cloudinary_files["resources"]
#             ]
#         except cloudinary.api.Error:
#             files = []

#     return render(request, "assistant_app/file_list.html", {
#         "files": files,
#         "selected_category": category
#     })


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
