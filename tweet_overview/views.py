# Create your views here.
import re

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from accounts.login_required import LoginRequiredMixin
from core.models import TwitterUser, Tweet, Source
from tweet_overview import forms
from tweet_overview.twitterapiclient import TwitterAPIClient


class IndexView(TemplateView):
    template_name = "tweet_overview/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tweets'] = Tweet.objects.filter(category=kwargs["category"])
        context['test'] = "Hello World!"

        return context


class NewTweetView(LoginRequiredMixin, FormView):
    template_name = "tweet_overview/new_tweet.html"
    form_class = forms.NewTweetForm
    success_url = reverse_lazy('tweet_overview:index', args={'category': 'politics'})

    def form_valid(self, form):
        twitter_api_client = TwitterAPIClient()
        #                Regex Fragment    | Meaning
        #                ============================
        #                        (       )         | group 1
        #                         status/          | matches exact status/
        #                                 (      ) | group 2
        #                                  [   ]   | Match characters that are...
        #                                   0-9    | ... a number,
        #                                       *  | 0 or more characters matching the rules above
        tweet_id = re.search('(status/)([0-9]*)', form.cleaned_data['twitter_url']).group(2)
        tweet_data = twitter_api_client.get_tweet_data(tweet_id)
        try:
            twitter_user = TwitterUser.objects.get(twitter_id=tweet_data['author_id'])
        except ObjectDoesNotExist:
            twitter_user_data = twitter_api_client.get_user_data(tweet_data['author_id'])
            twitter_user = TwitterUser.objects.create(
                twitter_id=tweet_data['author_id'],
                username=twitter_user_data['username'],
                name=twitter_user_data['name'],
                profile_image_url=twitter_user_data['profile_image_url']
            )
        tweet = Tweet.objects.create(
            twitter_id=tweet_data['id'],
            added_by=self.request.user,
            content=tweet_data['text'],
            twitter_user=twitter_user,
            category=form.cleaned_data['category']
        )

        Source.objects.create(
            link=form.cleaned_data['source_url'],
            tweet=tweet
        )

        return super().form_valid(form)
