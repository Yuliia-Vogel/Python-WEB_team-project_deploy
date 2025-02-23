from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
            # uploaded_file = form.save(commit=False)  # Не зберігаємо одразу
            # uploaded_file.user = request.user  # Додаємо користувача вручну
            # uploaded_file.save()  # Тепер зберігаємо
            # return redirect('files:file_list')  # редірект на список файлів
    else:
        form = UploadFileForm()
    return render(request, 'assistant_app/upload_file.html', {'form': form})


@login_required
def file_list(request):
    files = UploadedFile.objects.filter(user=request.user)  # Фільтруємо тільки файли поточного юзера
    return render(request, 'assistant_app/file_list.html', {'files': files})
