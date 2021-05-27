from django.urls import path, include
from store.views import index, test
from rest_framework import routers
from django.conf.urls.static import static



urlpatterns = [
    path('', index ,name='index'),
    path('test/', test, name='test')
] 