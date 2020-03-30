from django.shortcuts import render

def index(request):
    return render(request,'index.html')

def search_option(request):
    return render(request,'searchOption.html')