from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('/temptations', views.temptations, name='temptations'),
    path('/good_habits', views.good_habits, name='good_habits'),
    path('/temptations/statistics', views.temptations_statistics, name='temptations_statistics'),
    path('/good_habits/statistics', views.good_habits_statistics, name='good_habits_statistics'),
    ]