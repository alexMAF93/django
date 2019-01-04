from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name = 'index'),
    path('user_profile/', views.user_profile, name = 'user_profile'),
    path('apps/', views.apps, name = 'apps'),
    path('apps/jokes/', views.jokes, name = 'jokes'),
    path('apps/jokes/subscribe', views.subscribe_jokes, name='subscribe_jokes'),
    path('server/', views.server_details, name = 'server'),
    path('accounts/', include('django.contrib.auth.urls')),
]
