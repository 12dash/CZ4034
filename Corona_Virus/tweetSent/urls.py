from django.urls import path
from . import views

urlpatterns = [
    path('tweet_sentiments/', views.tweet_sentic, name='tweet_p_n'),
]
