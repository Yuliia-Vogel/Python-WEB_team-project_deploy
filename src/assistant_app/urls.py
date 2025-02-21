"""
URL configuration for assistant_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from .views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls", namespace="users")),  # Підключаємо маршрути користувачів
    path("notes/", include("notes.urls", namespace="notes")),  # Підключаємо маршрути нотаток
    path("contacts/", include("contacts.urls", namespace="contacts")),  # 📌 Додаємо namespace
    path('users/', include("users.urls", namespace="users")),
    path("", home, name="home"),  # Головна сторінка
]
