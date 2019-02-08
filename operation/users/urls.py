from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('login',views.loginone,name='login'),
    path('logout',views.logoutone,name='logout'),
    path('register',views.registerone,name='register'),
    path('user_center',views.userCenter,name='userCenter'),
    path('edit_profile',views.editProfile,name='editProfile'),
    path('change_password',views.changePassword,name='changePassword'),
    path('app_bar',views.appBar,name='appBar'),
]



