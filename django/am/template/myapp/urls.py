# myapp/urls.py
from django.urls import path
from myapp.views.device_api import device_add_api

urlpatterns = [
    path("api/device/add/", device_add_api),
]

