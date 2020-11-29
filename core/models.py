from django.conf import settings
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
    category = models.CharField(
        choices=settings.CATEGORY_CHOICES,
        max_length=255,
        default='other')


class Source(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    link = models.CharField(max_length=255)

    def current_vote_number(self):
        votes = Vote.objects.filter(
            source=self,
        )
        vote_result = 0
        for vote in votes:
            if vote.is_fitting is True:
                vote_result += 1
            else:
                vote_result -= 1
        return vote_result


class Vote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_fitting = models.BooleanField(max_length=255)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    text = models.TextField()
