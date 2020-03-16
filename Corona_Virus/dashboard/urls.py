from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_dashboard, name='show_dashboard'),
]
