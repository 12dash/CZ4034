"""Corona_Virus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index,  name = 'home'),
    path('searchOption/',views.search_option, name = 'option'),
    path('admin/', admin.site.urls),  
    path('dynamicSearch/', include('dynamicSearch.urls')),  
    path('search/', include ('search.urls')),
    path('sentiment/',include('Tweet_sentiment.urls')),
    path('sentiment/',views.option_sentiment, name = 's_option'),
    path('tweet_sentiment/',include('tweetSent.urls')),
    path('country_sentiment/',include('CountrySentiments.urls')),
    path('dyanmic_sentiment/',include('DynamicSentiments.urls')),
    path('static_sentiment/',include('Static_sentiments.urls')),
    path('image/',views.image_search,  name = 'image'),
    path('classification/',include('classification.urls')),
]
