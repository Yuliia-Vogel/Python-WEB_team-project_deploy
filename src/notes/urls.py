from django.urls import path
from .views import (
    NoteListView, NoteDetailView, NoteCreateView, NoteUpdateView, NoteDeleteView,
    TagListView, TagCreateView
)

urlpatterns = [
    path('', NoteListView.as_view(), name='note-list'),  # 📌 Всі нотатки
    path('<int:pk>/', NoteDetailView.as_view(), name='note-detail'),  # 📌 Окрема нотатка
    path('create/', NoteCreateView.as_view(), name='note-create'),  # 📌 Додавання
    path('<int:pk>/edit/', NoteUpdateView.as_view(), name='note-edit'),  # 📌 Редагування
    path('<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),  # 📌 Видалення
    path('tags/', TagListView.as_view(), name='tag-list'),  # 📌 Всі теги
    path('tags/create/', TagCreateView.as_view(), name='tag-create'),  # 📌 Додавання тегу
]