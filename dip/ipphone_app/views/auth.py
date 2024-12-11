from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, render

from utils import LogManager


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            LogManager.make_log(
                request=request,
                slug="login",
                by_user_id=request.user.id,
                user=user.username,
            )
            messages.success(request, "Вы успешно вошли в систему!")
            return redirect("home")
        else:
            messages.error(request, "Ошибка входа. Попробуйте еще раз.")
            return redirect("login")
    else:
        return render(request, "common/login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect("home")
