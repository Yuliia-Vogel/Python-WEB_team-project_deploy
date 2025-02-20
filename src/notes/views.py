from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Note, Tag
from .forms import NoteForm, TagForm
from django.db.models import Q

# 📌 Вивід усіх нотаток
class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        queryset = Note.objects.filter(user=self.request.user)
        tag = self.request.GET.get("tag")  # Фільтр за тегом
        search_query = self.request.GET.get("q")  # Пошуковий запит

        if tag:
            queryset = queryset.filter(tags__name=tag)
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        context["search_query"] = self.request.GET.get("q", "")  # Передача пошуку в шаблон
        return context

# 📌 Детальний перегляд нотатки
class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'

# 📌 Додавання нової нотатки
class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes:note-list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # ✅ Додаємо користувача перед збереженням
        return super().form_valid(form)

# 📌 Оновлення нотатки
class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes:note-list')

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('notes:note-list')

# 📌 Вивід усіх тегів
class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'notes/tag_list.html'
    context_object_name = 'tags'

# 📌 Додавання тегу
class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'notes/tag_form.html'
    success_url = reverse_lazy('notes:tag-list')

# 📌 Видалення тегу
class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = "notes/tag_confirm_delete.html"
    success_url = reverse_lazy("notes:tag-list")