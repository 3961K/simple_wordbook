from django.views.generic import TemplateView


class ForbiddenView(TemplateView):
    template_name = 'error_front/403.html'
