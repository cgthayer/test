from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView

# app_name = 'userlinks'

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='eg/index.html')),
]

