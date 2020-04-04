from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('programari/<date>/<day>', views.make_appointment, name='make_appointment'),
    path('edi/', views.admin_page, name='admin_page'),
    ]