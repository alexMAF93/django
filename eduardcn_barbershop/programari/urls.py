from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name = 'index'),
    path('programari/<date>/', views.make_programare, name = 'make_programare'),
    path('edi/', views.admin, name = 'admin'),
]
