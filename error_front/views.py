from django.views.generic import TemplateView


class ForbiddenView(TemplateView):
    template_name = 'error_front/403.html'


class NotFoundView(TemplateView):
    template_name = 'error_front/404.html'
