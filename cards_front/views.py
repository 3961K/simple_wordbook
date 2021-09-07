from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class CardsView(TemplateView):
    template_name = 'cards_front/cards.html'


class CardView(TemplateView):
    template_name = 'cards_front/card.html'


class CardCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'cards_front/new_card.html'
