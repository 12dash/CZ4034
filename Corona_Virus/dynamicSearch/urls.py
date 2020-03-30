from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dsearch, name='dynamic_search'),
    path('dynamic_result/',views.Dsearch_output, name = 'dynamic_results')
]
