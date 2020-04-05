from django.urls import path
from . import views

urlpatterns = [
    path('static_sentiment/', views.Ssearch, name='static_sent'),
    path('static_sentiment_r/', views.Ssearch_output, name='static_sent_r'),
]
