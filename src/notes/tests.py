from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Note, Tag
from .forms import NoteForm, TagForm
from .views import (
    NoteListView, NoteDetailView, NoteCreateView, NoteUpdateView, NoteDeleteView,
    TagListView, TagCreateView, TagDeleteView
)

User = get_user_model()

#Тести моделей
class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Test Tag")

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, "Test Tag")

    def test_tag_str_method(self):
        self.assertEqual(str(self.tag), "Test Tag")

class NoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.tag = Tag.objects.create(name="Test Tag")
        self.note = Note.objects.create(user=self.user, title="Test Note", content="This is a test note.")
        self.note.tags.add(self.tag)

    def test_note_creation(self):
        self.assertEqual(self.note.title, "Test Note")
        self.assertEqual(self.note.content, "This is a test note.")
        self.assertEqual(self.note.user.username, "testuser")
        self.assertIn(self.tag, self.note.tags.all())

    def test_note_str_method(self):
        self.assertEqual(str(self.note), "Test Note")

#Тести форм
class NoteFormTest(TestCase):
    def test_valid_note_form(self):
        form = NoteForm(data={
            'title': 'Test Note',
            'content': 'This is a test note content.',
            'tags': []
        })
        self.assertTrue(form.is_valid())

    def test_invalid_note_form(self):
        form = NoteForm(data={})
        self.assertFalse(form.is_valid())

class TagFormTest(TestCase):
    def test_valid_tag_form(self):
        form = TagForm(data={'name': 'New Tag'})
        self.assertTrue(form.is_valid())

    def test_invalid_tag_form(self):
        form = TagForm(data={'name': ''})
        self.assertFalse(form.is_valid())

#Тести views
class NoteViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.tag = Tag.objects.create(name="Test Tag")
        self.note = Note.objects.create(user=self.user, title="Test Note", content="This is a test note.")
        self.note.tags.add(self.tag)

    def test_note_list_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('notes:note-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")
        self.assertTemplateUsed(response, 'notes/note_list.html')

    def test_note_detail_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('notes:note-detail', args=[self.note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is a test note.")
        self.assertTemplateUsed(response, 'notes/note_detail.html')

    def test_note_create_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('notes:note-create'), {
            'title': 'New Note',
            'content': 'New note content',
            'tags': [self.tag.id]
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(Note.objects.count(), 2)

    def test_note_delete_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('notes:note-delete', args=[self.note.id]))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(Note.objects.count(), 0)

#Тести URL
class TestUrls(SimpleTestCase):
    def test_note_list_url_resolves(self):
        url = reverse('notes:note-list')
        self.assertEqual(resolve(url).func.view_class, NoteListView)

    def test_note_detail_url_resolves(self):
        url = reverse('notes:note-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, NoteDetailView)

    def test_note_create_url_resolves(self):
        url = reverse('notes:note-create')
        self.assertEqual(resolve(url).func.view_class, NoteCreateView)

    def test_note_delete_url_resolves(self):
        url = reverse('notes:note-delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, NoteDeleteView)

    def test_tag_list_url_resolves(self):
        url = reverse('notes:tag-list')
        self.assertEqual(resolve(url).func.view_class, TagListView)