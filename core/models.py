from django.db import models

from accounts.models import User


class TwitterUser(models.Model):
    twitter_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    profile_image_url = models.CharField(max_length=255)


class Tweet(models.Model):
    twitter_id = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    twitter_user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)


class Source(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    link = models.CharField(max_length=255)


class Vote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_fitting = models.CharField(max_length=255)
