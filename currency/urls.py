from django.contrib import admin
from django.urls import path, include,re_path
from . import views

urlpatterns = [
    path('',views.homepage,name="home"),
    path('add/',views.maintable,name = 'details'),
    path('crypto/<name>/',views.details,name = 'details'),
    re_path(r'^converter/$', views.conv, name='urlname')

]