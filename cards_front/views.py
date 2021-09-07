from django.views.generic import TemplateView


class CardsView(TemplateView):
    template_name = 'cards_front/cards.html'
