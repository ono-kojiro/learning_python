from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

import yaml

def index(request):
  return HttpResponse("API server is running.")

urlpatterns = [
  path('', index),
  path('admin/', admin.site.urls),
]

items = yaml.safe_load(open("myproject/urlpatterns.yml"))
for item in items:
    urlpattern = path('', include(item))
    urlpatterns.append(urlpattern)

