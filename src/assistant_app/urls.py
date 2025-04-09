from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.http import JsonResponse # для дебагу
from .views import home
from django.conf import settings
from django.conf.urls.static import static
from .settings import ALLOWED_HOSTS

def debug_allowed_hosts(request): # для дебагу
    return JsonResponse({"ALLOWED_HOSTS": ALLOWED_HOSTS}) 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls", namespace="users")),  # Підключаємо маршрути користувачів
    path("notes/", include("notes.urls", namespace="notes")),  # Підключаємо маршрути нотаток
    path("contacts/", include("contacts.urls", namespace="contacts")),  # 📌 Додаємо namespace
    # path('users/', include("users.urls", namespace="users")),
    path("news/", include("news.urls")), # Підлючаємо маршрут новин
    path('files/', include('files.urls', namespace="files")), # Підключаємо маршрути для файлів
    path("", home, name="home"),  # Головна сторінка
    path("debug-allowed-hosts/", lambda request: JsonResponse({"allowed_hosts": settings.ALLOWED_HOSTS})),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
