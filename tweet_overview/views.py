from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from accounts.login_required import LoginRequiredMixin


class IndexView(TemplateView):
    template_name = "tweet_overview/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = "Hello World!"

        return context


class NewTweetView(LoginRequiredMixin, TemplateView):
    template_name = "tweet_overview/new_tweet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

