from django.db import models
from django.contrib.auth import get_user_model
import cloudinary
import cloudinary.uploader
import cloudinary.models

User = get_user_model()

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    file = cloudinary.models.CloudinaryField('file', resource_type='auto')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File {self.id} uploaded by {self.user}"
