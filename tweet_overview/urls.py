from django.contrib import admin
from django.urls import path, include

from tweet_overview import views

app_name="tweet_overview"

urlpatterns = [
    path('new_tweet', views.NewTweetView.as_view(), name="new_tweet"),
    path('<category>', views.IndexView.as_view(), name="index"),
]