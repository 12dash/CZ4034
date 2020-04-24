from django.http import HttpResponseRedirect

from django.views.generic import TemplateView
from django.shortcuts import render
import pysolr

import time
# Create your views here.


def search(request):
    print(request.GET)
    return render(request, 'search.html')

def search_select(request):
    return render(request, 'static_select.html')

def custom_search(request):
    return render(request, 'custom_search.html')

def rerank_q(request):
    query = request.GET['search']
    custom = request.GET['search_param']
    a = 'tweet:'+ "\""+ query +"\"" 
    b = 'tweet:'+ "\""+ custom+"\""
    data = rerank(a,b)
    return render(request, 'newpage.html', {'data': data})


def custom_search_output(request):
    query = request.GET['search']
    custom = request.GET['search_param']
    query = 'tweet:'+ "\""+ query +"\"" 
    b = 'location:'+ "\""+ custom+"\""

    s = time.time()
    data = solr_custom_search(query,b)
    e = time.time()
    elapsed_time = e-s
    print(elapsed_time)

    return render(request, 'custom_result.html', {'data': data, 'length': len(data)})

def search_output(request):
    query = request.GET['search']   
    query = 'tweet:'+ "\""+ query +"\""    
    print(query)

    s = time.time()
    data = solr_search(query)
    e = time.time()
    elapsed_time = e-s
    print(elapsed_time)

    return render(request, 'newpage.html', {'data': data})


def solr_search(a):
    solr = pysolr.Solr('http://localhost:8983/solr/tweets', timeout=10)     
    results = solr.search(a,rows = 20, f1 = "*,score", sort="likes desc")
    print(results)
    return results

def solr_custom_search(a,b):
    solr = pysolr.Solr('http://localhost:8983/solr/tweets', timeout=10)     
    results = solr.search(a,rows = 20, fq = b, sort="likes desc")
    print(results)
    return results

def rerank(a,b):
    solr = pysolr.Solr('http://localhost:8983/solr/tweets', timeout=10)
    params = {
        'rq':'{!rerank reRankQuery=$rqq reRankDocs=1000 reRankWeight=3}',
        'rqq':b,
    }
    results = solr.search(a, **params)
    print(results)
    return results