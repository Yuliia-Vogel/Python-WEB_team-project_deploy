# import logging
# from django.db import models
# from django.contrib.auth import get_user_model
# import cloudinary
# import cloudinary.uploader
# import cloudinary.models

# logger = logging.getLogger(__name__)

# User = get_user_model()

# class UploadedFile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
#     file = cloudinary.models.CloudinaryField('file', overwrite=False, resource_type='auto')
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self, *args, **kwargs):
#         """Змінюємо шлях до файлу, додаючи окрему папку для кожного користувача перед збереженням."""
#         if not self.file:  # Якщо файл ще не завантажено, то повертається None
#             return
        
#         folder_name = f"user_{self.user.id}"  # Створюємо унікальну папку для юзера
#         uploaded_file = cloudinary.uploader.upload(
#             self.file,
#             folder=folder_name,  # Задаємо папку
#             resource_type="auto"
#         )

#         logger.info(f"Uploading file for user {self.user.id} to folder {folder_name}")

#         self.file = uploaded_file["secure_url"]  # Зберігаємо URL файлу
#         super().save(*args, **kwargs) # зберігаю файли
    
#     def __str__(self):
#         return f"File {self.id} uploaded by {self.user}"


# class File(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     file = models.URLField()  # Тут більше не FileField, а URLField!
#     uploaded_at = models.DateTimeField(auto_now_add=True)


import logging
from django.db import models
from django.contrib.auth import get_user_model
import cloudinary
import cloudinary.uploader
import cloudinary.models

logger = logging.getLogger(__name__)

User = get_user_model()

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    file_url = models.URLField()  # Зберігаємо лише URL замість файлу
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Завантажуємо файл у Cloudinary та сортуємо по папках."""
        if not self.file_url:  # Якщо URL ще не збережений, завантажуємо файл
            uploaded_file = kwargs.pop('file', None)
            if uploaded_file:
                file_extension = uploaded_file.name.split('.')[-1].lower()

                # Визначаємо папку за типом файлу
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    file_type = 'images'
                elif file_extension in ['pdf', 'doc', 'docx', 'txt']:
                    file_type = 'documents'
                elif file_extension in ['mp4', 'avi', 'mov']:
                    file_type = 'videos'
                else:
                    file_type = 'others'

                # Створюємо унікальну папку для користувача
                folder_name = f"user_{self.user.id}/{file_type}"
                uploaded_data = cloudinary.uploader.upload(uploaded_file, folder=folder_name)

                logger.info(f"Uploaded file for user {self.user.id} to folder {folder_name}")

                self.file_url = uploaded_data["secure_url"]  # Зберігаємо тільки URL

        super().save(*args, **kwargs)

    def __str__(self):
        return f"File uploaded by {self.user}"
