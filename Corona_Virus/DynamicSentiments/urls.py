from django.urls import path
from . import views

urlpatterns = [
    path('dynamic_sentiment/', views.Dysearch, name='dynamic_sent'),
    path('dynamic_sentiment_r/', views.Dysearch_output, name='dynamic_sent_r'),
]
