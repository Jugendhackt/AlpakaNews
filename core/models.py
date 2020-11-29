from django.conf import settings
from django.db import models

from accounts.models import User


class TwitterUser(models.Model):
    twitter_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    profile_image_url = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)


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

    def current_upvotes(self):
        return Vote.objects.filter(
            source=self,
            is_fitting=True
        ).count()

    def current_downvotes(self):
        return Vote.objects.filter(
            source=self,
            is_fitting=False
        ).count()

    def is_link_verified(self):
        for source in settings.VERIFIED_SOURCES:
            if source in self.link:
                return True

class Vote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_fitting = models.BooleanField(max_length=255)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
