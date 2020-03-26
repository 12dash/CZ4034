from django.http import HttpResponseRedirect

from django.views.generic import TemplateView
from django.shortcuts import render
import pysolr

# Create your views here.


def search(request):
    print(request.GET)
    return render(request, 'search.html')

def search_output(request):
    query = request.GET['search']   
    query = 'tweet:'+ "\""+ query +"\""    
    print(query)
    data = solr_search(query)
    for result in data:
        print(result['tweet'])
    return render(request, 'newpage.html', {'data': data})


def solr_search(a):
    solr = pysolr.Solr('http://localhost:8983/solr/tweets', timeout=10)    
    results = solr.search(a)
    return results
