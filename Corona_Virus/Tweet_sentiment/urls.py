from django.urls import path
from . import views

urlpatterns = [
    path('', views.finding_posistive_tweets , name='sentiment_p_n'),    
]
