

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import update_last_login

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser
from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_str

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse

from rest_framework import generics, status, permissions, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView

from .forms import UserFileForm
from .models import UserFile, CustomUser
from .serializers import RegisterSerializer, LoginSerializer
from django.conf import settings


User = get_user_model()

# 🌐 HTML СТОРІНКИ

def register_page(request):
    return render(request, "register.html")

def registration_success_view(request):
    return render(request, "registration_success.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Ви успішно увійшли до системи!")
            return redirect("home")
        else:
            messages.error(request, "Невірне ім'я користувача або пароль.")

    return render(request, "login.html")

def password_reset_form_view(request):
    return render(request, "password_reset_form.html")

def password_reset_done_view(request):
    return render(request, "password_reset_done.html")

def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            messages.success(request, "Пароль успішно змінено!")
            return redirect("password_reset_complete")
        else:
            messages.error(request, "Токен недійсний або користувача не знайдено.")
            return redirect("password_reset_confirm", uidb64=uidb64, token=token)

    return render(request, "password_reset_confirm.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Ви успішно вийшли з системи.")
    return redirect("login_page")

def password_reset_sent_view(request):
    return render(request, "password_reset_sent.html")


def password_reset_complete_view(request):
    return render(request, "password_reset_complete.html")

# 📥 API Views

### 🔹 РЕЄСТРАЦІЯ
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            error_messages = []
            
            if 'username' in errors:
                error_messages.append(f"Ім'я користувача: {errors['username'][0]}")
            if 'email' in errors:
                error_messages.append(f"Електронна пошта: {errors['email'][0]}")
            if 'password' in errors:
                error_messages.append(f"Пароль: {errors['password'][0]}")
            
            for msg in error_messages:
                messages.error(request, msg)
            
            return redirect('register_page')

        serializer.save()
        messages.success(request, "Ваш акаунт успішно створено! Увійдіть до системи, щоб скористатися функціоналом.")
        return redirect("registration_success")


### 🔹 ЛОГІН
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

### 🔹 ЗМІНА ПАРОЛЯ
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        old_password = serializers.CharField(write_only=True)
        new_password = serializers.CharField(write_only=True)

        def validate_new_password(self, value):
            validate_password(value)
            return value

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"old_password": ["Wrong password."]}, status=400)

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response({"message": "Password updated successfully!"})

### 🔹 ВІДНОВЛЕННЯ ПАРОЛЯ (НАДСИЛАННЯ EMAIL)
from django.urls import reverse

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Генеруємо токен
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://127.0.0.1:8000/api/users/password-reset-confirm/{uid}/{token}/"

        # Надсилаємо email
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        # Перенаправлення на сторінку з підтвердженням
        return redirect("password_reset_sent")



### 🔹 ВІДНОВЛЕННЯ ПАРОЛЯ (ПІДТВЕРДЖЕННЯ)
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    class InputSerializer(serializers.Serializer):
        new_password = serializers.CharField(write_only=True)

        def validate_new_password(self, value):
            validate_password(value)
            return value

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"message": "Password has been reset successfully!"}, status=status.HTTP_200_OK)


@login_required
def upload_file(request):
    if request.method == "POST":
        form = UserFileForm(request.POST, request.FILES)
        if form.is_valid():
            user_file = form.save(commit=False)
            user_file.user = request.user  # Прив'язуємо файл до користувача
            user_file.save()
            return redirect("users:file_list")  # Після завантаження переходимо до списку файлів
    else:
        form = UserFileForm()

    return render(request, "users/upload_file.html", {"form": form})

@login_required
def file_list(request):
    files = UserFile.objects.filter(user=request.user)
    return render(request, "users/file_list.html", {"files": files})
  
#         return redirect("password_reset_complete")
