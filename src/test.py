from django.core.mail import send_mail

send_mail(
    'Тестове повідомлення',
    'Це тестовий лист від Django.',
    'app.1.foruse@gmail.com',
    ['arwen.vogel@gmail.com'],
    fail_silently=False,
)