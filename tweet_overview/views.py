from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from accounts.login_required import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "tweet_overview/index.html"
