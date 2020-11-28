from django import forms


class NewTweetForm(forms.Form):
    twitter_url = forms.CharField(
        label="Link zum Tweet:",
        required=True
    )
    source_url = forms.CharField(
        label="Link zu einer Quelle:",
        required=True
    )
