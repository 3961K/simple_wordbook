from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = 'authentication_front/login.html'
