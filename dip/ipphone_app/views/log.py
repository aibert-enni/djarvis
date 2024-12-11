from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from ipphone_app.models import Log


class LogListView(LoginRequiredMixin, ListView):
    model = Log
    template_name = "log/logs.html"
    context_object_name = "logs"


class LogDetailView(LoginRequiredMixin, DetailView):
    model = Log
    template_name = "log/log.html"
    context_object_name = "log"
