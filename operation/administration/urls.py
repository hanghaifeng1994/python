from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('systeminfo',views.systeminfo,name='systeminfo'),
    path('othersys',views.othersys,name='othersys'),
    path('delpid',views.delpid,name='delpid')
]