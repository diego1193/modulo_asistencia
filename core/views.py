# core/views.py
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = "core/login.html"
