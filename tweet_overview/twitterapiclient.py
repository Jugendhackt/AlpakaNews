from django.conf import settings
from TwitterAPI import TwitterAPI


class TwitterAPIClient:
    def __init__(self):
        self.api = TwitterAPI(
            settings.TWITTER_CONSUMER_KEY,
            settings.TWITTER_CONSUMER_SECRET,
            settings.TWITTER_ACCESS_TOKEN,
            settings.TWITTER_ACCESS_TOKEN_SECRET,
            api_version='2'
        )

    def get_tweet_data(self, tweet_id):
        r = self.api.request(f'tweets/:{tweet_id}', {
            'tweet.fields': 'author_id,entities,created_at'
        })
        for item in r:
            return item

    def get_user_data(self, user_id):
        r = self.api.request(f'users/:{user_id}', {
            'user.fields': 'id,name,username,profile_image_url,verified'
        })
        for item in r:
            return item
