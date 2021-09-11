from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class WordbooksView(TemplateView):
    template_name = 'wordbooks_front/wordbooks.html'


class WordbookView(TemplateView):
    template_name = 'wordbooks_front/wordbook.html'


class WordbookCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'wordbooks_front/new_wordbook.html'
