from django.urls import path

from tweet_overview import views

app_name = "tweet_overview"

urlpatterns = [
    path('new_tweet/', views.NewTweetView.as_view(), name="new_tweet"),
    path('add_comment/', views.AddComment.as_view(), name="add_comment"),
    path('vote/<str:id>/<is_fitting>/', views.VoteView.as_view(), name="vote"),
    path('<category>/', views.IndexView.as_view(), name="index"),
]
