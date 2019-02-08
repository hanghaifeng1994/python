from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('user_add',views.useradd,name='user_add'),
    path('group_add',views.groupadd,name='group_add'),
    path('add_group',views.addgroup,name='add_group'),
    path('user_to_group',views.usertogroup,name='user_to_group'),
    path('permission',views.permission,name='permission'),
    path('virus_scanning',views.virusscanning,name="virus_scanning"),
]