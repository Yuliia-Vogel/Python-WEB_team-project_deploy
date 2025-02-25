from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()

class UserTests(TestCase):
    
    def setUp(self):
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login_page')
        self.logout_url = reverse('users:logout')
        self.password_reset_url = reverse('users:password_reset')
        self.password_reset_done_url = reverse('users:password_reset_done')
        self.password_reset_sent_url = reverse('users:password_reset_sent')
        self.password_reset_complete_url = reverse('users:password_reset_complete')

        self.user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'NewPassword123',
            'password': 'NewPassword123'
        }
        
        self.user_login_data = {
            'username': 'newuser',
            'password': 'NewPassword123'
        }

        # Створюємо користувача для тестування логіну/логауту
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='TestPassword123'
        )

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, follow=True)
    
        if response.status_code != 302:
            print("❌ Статус-код не відповідає 302 (Redirect). Фактичний статус-код:", response.status_code)
            print("📄 Вміст відповіді:", response.content.decode())

        self.assertRedirects(response, reverse('users:registration_success'),
                         msg_prefix="❌ Невірний редирект після реєстрації користувача.")
    
        self.assertTrue(User.objects.filter(username='newuser').exists(), 
                    "❌ Користувач 'newuser' не створений у базі даних.")
    
        print("✅ Користувач 'newuser' успішно створений у базі даних.")

        
    def test_login_user(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'TestPassword123'
        })
        self.assertEqual(response.status_code, 302)  # Очікуємо редирект після успішного логіну
        self.assertRedirects(response, reverse('home'))
        print("✅ Логін працює коректно.")

    def test_logout_user(self):
        self.client.login(username='testuser', password='TestPassword123')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, reverse('users:login_page'))
        print("✅ Логаут працює коректно.")

    def test_password_reset_request(self):
        response = self.client.post(self.password_reset_url, {'email': 'testuser@example.com'})
        self.assertRedirects(response, self.password_reset_sent_url)
        print("✅ Запит на відновлення пароля працює коректно.")

    def test_password_reset_complete(self):
        response = self.client.get(self.password_reset_complete_url)
        self.assertEqual(response.status_code, 200)
        print("✅ Сторінка успішного відновлення пароля доступна.")


class AccessControlTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Створюємо тестового користувача
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='TestPassword123'
        )

        # URL-адреси для тестування
        self.home_url = reverse('home')
        self.notes_url = reverse('notes:note-list')
        self.contacts_url = reverse('contacts:contact-list')
        self.files_url = reverse('files:file_list')

        self.login_url = reverse('users:login_page')

    def test_access_allowed_for_authenticated_user(self):
        print("🔍 Перевірка доступу для авторизованого користувача...")
        self.client.login(username='testuser', password='TestPassword123')

        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        
        # Перевірка відображення функціоналу для авторизованого користувача
        self.assertContains(response, 'Вийти')
        self.assertContains(response, 'Notes')
        self.assertContains(response, 'Contacts')
        self.assertContains(response, 'Files')

        print("✅ Доступ для авторизованого користувача відображається коректно.")

    def test_access_denied_for_anonymous_user(self):
        print("🔍 Перевірка доступу для неавторизованого користувача...")
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        
        # Перевірка, що доступні лише кнопки "Увійти" та "Реєстрація"
        self.assertContains(response, 'Реєстрація')
        self.assertContains(response, 'Увійти')
        
        # Перевірка, що кнопка "Вийти" НЕ відображається
        self.assertNotContains(response, 'Вийти')
        
        # Перевірка, що кнопки "Notes", "Contacts", "Files" НЕ відображаються
        self.assertNotContains(response, 'Notes')
        self.assertNotContains(response, 'Contacts')
        self.assertNotContains(response, 'Files')
        
        print("✅ Доступ для неавторизованого користувача обмежений коректно.")
