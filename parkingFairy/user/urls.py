from django.contrib import admin
from django.urls import path, include
from user import views

urlpatterns = [

    path('signup/', views.index, name='signup'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),



]
