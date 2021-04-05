from django.urls import path
from . import views


urlpatterns = [
    path('show', views.show, name='show'),
    path('home', views.home, name='home'),
    path('index', views.index, name='index')
]
