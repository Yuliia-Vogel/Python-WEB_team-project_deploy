from django.test import TestCase
from django.urls import reverse

class NewsPageTests(TestCase):
    def test_news_page_status_code(self):
        """Перевірка, чи сторінка новин повертає статус-код 200"""
        response = self.client.get(reverse('news:news_summary'))
        self.assertEqual(response.status_code, 200)

    def test_news_page_template(self):
        """Перевірка, чи використовується правильний шаблон"""
        response = self.client.get(reverse('news:news_summary'))
        self.assertTemplateUsed(response, 'news/news_summary.html')

    def test_news_page_content(self):
        """Перевірка, чи сторінка містить заголовок 'Новини'"""
        response = self.client.get(reverse('news:news_summary'))
        self.assertContains(response, "<h2>Новини</h2>", html=True)
