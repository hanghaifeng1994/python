from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('iplen',views.iplen,name='iplan'),
    path('ipinput',views.ipinput,name='ipinput'),
    path('pyweb',views.pyweb,name='pyweb')
]