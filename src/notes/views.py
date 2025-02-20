from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Note, Tag
from .forms import NoteForm, TagForm

# 📌 Вивід усіх нотаток
class NoteListView(ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    
    def get_queryset(self):
        queryset = Note.objects.filter(user=self.request.user)  # Тільки нотатки поточного користувача
        tag = self.request.GET.get("tag")  # Отримуємо тег з параметрів URL
        if tag:
            queryset = queryset.filter(tags__name=tag)  # Фільтруємо за тегом
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()  # Додаємо всі теги в шаблон
        return context

# 📌 Детальний перегляд нотатки
class NoteDetailView(DetailView):
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'

# 📌 Додавання нової нотатки
class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('note-list')

# 📌 Редагування нотатки
class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('note-list')

# 📌 Видалення нотатки
class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('note-list')

# 📌 Вивід усіх тегів
class TagListView(ListView):
    model = Tag
    template_name = 'notes/tag_list.html'
    context_object_name = 'tags'

# 📌 Додавання тегу
class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'notes/tag_form.html'
    success_url = reverse_lazy('tag-list')
    
# 📌 Видалення тегу
class TagDeleteView(DeleteView):
    model = Tag
    template_name = "notes/tag_confirm_delete.html"
    success_url = reverse_lazy("tag-list")