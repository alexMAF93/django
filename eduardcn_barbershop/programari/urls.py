from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name = 'index'),
    path('programari/<date>/', views.make_programare, name = 'make_programare'),
    path('admin/', views.admin, name = 'admin'),
]
