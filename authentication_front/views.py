from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = 'authentication_front/login.html'


class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'authentication_front/logout.html'
