from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('devices/', views.device_list, name='device_list'),
    path('devices/add/', views.device_add, name='device_add'),
    path('devices/delete/<int:pk>/', views.device_delete, name='device_delete'),
]

