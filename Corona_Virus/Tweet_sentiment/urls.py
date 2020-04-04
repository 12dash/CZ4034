from django.urls import path
from . import views

urlpatterns = [
    path('keyword_option/', views.tweet_option, name='sentiment_p_n'),
    path('corona/', views.corona, name='corona'),
    path('epidemic/', views.epidemic, name='epidemic'),
    path('safe/', views.safe, name='safe'),
    path('quarantine/', views.quarantine, name='quarantine'),
    path('contagious/', views.contagious, name='contagious'),
    path('china/', views.china, name='china'),
]
