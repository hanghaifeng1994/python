from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('orlvnc',views.orlvnc,name='orlvnc'),
    path('datato',views.datato,name='datato'),
    path('outooracle',views.autooracle,name='autooracle')
]