import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from orders.models import Order

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import User


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.verification_token = str(uuid.uuid4())
            user.save()

            verification_link = (
                f"http://127.0.0.1:8000/users/verify/{user.verification_token}/"
            )
            send_mail(
                "Подтверждение регистрации",
                f"Привет, {user.email}!\nПерейдите по ссылке для подтверждения регистрации:\n{verification_link}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return redirect("users:user_login")
    else:
        form = UserRegistrationForm()

    return render(request, "users/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if not user.is_verified:
                    form.add_error(None, "Email не подтверждён. Проверьте почту.")
                else:
                    login(request, user)
                    return redirect("users:profile")
            else:
                form.add_error(None, "Неверный email или пароль.")
    else:
        form = UserLoginForm()

    return render(request, "users/login.html", {"form": form})


@login_required(login_url="/users/login")
def user_logout(request):
    logout(request)
    return redirect("users:user_login")


@login_required(login_url="/users/login")
def profile(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users:profile")

    else:
        form = UserProfileForm(instance=user)
    orders = Order.objects.filter(user=user)

    return render(
        request,
        "users/profile.html",
        {
            "form": form,
            "orders": orders,
        },
    )


User = get_user_model()


def verify_email(request, token):
    try:
        user = User.objects.get(verification_token=token)
        user.is_active = True  # Активируем пользователя
        user.is_verified = True  # Помечаем как верифицированного
        user.verification_token = None  # Очищаем токен
        user.save()
        messages.success(request, "Ваш email успешно подтверждён! Теперь можно войти.")
        return redirect("users:user_login")
    except User.DoesNotExist:
        messages.error(request, "Неверный или устаревший токен.")
        return render(request, "users/verification_failed.html")
