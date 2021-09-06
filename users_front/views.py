from django.views.generic import TemplateView


class UsersView(TemplateView):
    template_name = 'users_front/users.html'


class UserCardsView(TemplateView):
    template_name = 'users_front/user_cards.html'
