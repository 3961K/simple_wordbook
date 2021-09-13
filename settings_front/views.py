from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class UserinfoUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'settings_front/user_info.html'
