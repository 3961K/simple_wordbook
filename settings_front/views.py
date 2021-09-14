from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class UserInfoUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'settings_front/user_info.html'


class UserPasswordChangeView(LoginRequiredMixin, TemplateView):
    template_name = 'settings_front/password_change.html'


class UserCardsView(LoginRequiredMixin, TemplateView):
    template_name = 'settings_front/cards.html'


class UserCardView(LoginRequiredMixin, TemplateView):
    template_name = 'settings_front/card.html'
