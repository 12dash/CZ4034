from django.shortcuts import render

def index(request):
    return render(request,'index.html')

def search_option(request):
    return render(request,'searchOption.html')

def option_sentiment(request):
    return render(request, 'Sentiment_option.html')

def image_search(request):
    return render(request, "image.html")