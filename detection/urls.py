from django.urls import path

from . import views

urlpatterns = [
    path('detection/',views.reg,name='check'),
    path('', views.index, name='index'),
]