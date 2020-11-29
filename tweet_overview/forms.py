from django import forms
from django.conf import settings
from django.core.validators import URLValidator


class NewTweetForm(forms.Form):
    twitter_url = forms.CharField(
        label="Link zum Tweet:",
        validators=[URLValidator(schemes=['https'])],
        required=True
    )
    source_url = forms.CharField(
        label="Link zu einer Quelle:",
        validators=[URLValidator(schemes=['https'])],
        required=True
    )

    category = forms.ChoiceField(
        choices=settings.CATEGORY_CHOICES,
        required=True
    )


class AddCommentForm(forms.Form):
    text = forms.CharField(
        label="Kommentartext:",
        required=True
    )
    tweet_id = forms.CharField(
        required=True
    )
    category = forms.CharField(
        required=True
    )
