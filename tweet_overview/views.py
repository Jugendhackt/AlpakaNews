# Create your views here.
import re

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import FormView, TemplateView
from django.views.generic.base import View

from accounts.login_required import LoginRequiredMixin
from core.models import Comment, Source, Tweet, TwitterUser, Vote
from tweet_overview import forms
from tweet_overview.twitterapiclient import TwitterAPIClient


class IndexView(TemplateView):
    template_name = "tweet_overview/index.html"

    def get_context_data(self, **kwargs):
        tweets = Tweet.objects.filter(
            category=kwargs["category"]).order_by('-id')
        context = super().get_context_data(**kwargs)

        context['tweets'] = tweets
        context['add_comment_form'] = forms.AddCommentForm()

        if self.request.GET.get('message') is not None:
            context['warning_message'] = self.request.GET.get('message')

        return context


class NewTweetView(LoginRequiredMixin, FormView):
    template_name = "tweet_overview/new_tweet.html"
    form_class = forms.NewTweetForm

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
        tweet_id = re.search(
            '(status/)([0-9]*)',
            form.cleaned_data['twitter_url']).group(2)
        tweet_data = twitter_api_client.get_tweet_data(tweet_id)
        try:
            twitter_user = TwitterUser.objects.get(
                twitter_id=tweet_data['author_id'])
        except ObjectDoesNotExist:
            twitter_user_data = twitter_api_client.get_user_data(
                tweet_data['author_id'])
            twitter_user = TwitterUser.objects.create(
                twitter_id=tweet_data['author_id'],
                username=twitter_user_data['username'],
                name=twitter_user_data['name'],
                profile_image_url=twitter_user_data['profile_image_url'],
                verified=twitter_user_data['verified']
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

        return redirect(
            'tweet_overview:index',
            category=form.cleaned_data['category'])


class VoteView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        if kwargs['is_fitting'] == "True" or kwargs['is_fitting'] == "true":
            is_fitting = True
        else:
            is_fitting = False
        try:
            current_vote = Vote.objects.get(
                source_id=kwargs['id'], user=self.request.user)
            if current_vote.is_fitting != is_fitting:
                current_vote.is_fitting = is_fitting
                current_vote.save()
        except ObjectDoesNotExist:
            Vote.objects.create(
                source_id=kwargs['id'],
                user=self.request.user,
                is_fitting=is_fitting
            )

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class AddComment(LoginRequiredMixin, View):
    form_class = forms.AddCommentForm

    def post(self, *args, **kwargs):
        form = forms.AddCommentForm(self.request.POST)
        if form.is_valid():
            Comment.objects.create(
                author=self.request.user,
                tweet_id=form.cleaned_data['tweet_id'],
                text=form.cleaned_data['text']
            )
            return redirect(
                'tweet_overview:index',
                category=form.cleaned_data['category'])
        else:
            base_url = reverse_lazy(
                'tweet_overview:index', kwargs={
                    'category': form.cleaned_data['category']})
            warning_message = urlencode(
                {'message': "Da ist wohl was schiefgelaufen, bitte versuche es erneut"})
            return redirect(f'{base_url}?{warning_message}')
