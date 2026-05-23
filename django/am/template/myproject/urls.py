from django.contrib import admin
from django.urls import path, include

import yaml

urlpatterns = [
  path('admin/', admin.site.urls),
]

items = yaml.safe_load(open("myproject/urlpatterns.yml"))
for item in items:
    urlpattern = path('', include(item))
    urlpatterns.append(urlpattern)

