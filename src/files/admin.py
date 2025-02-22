from django.contrib import admin
# from django.contrib.auth.decorators import login_required
from .models import UploadedFile

@admin.register(UploadedFile)
# @login_required
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'uploaded_at')
