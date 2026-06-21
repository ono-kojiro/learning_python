#!/bin/bash
set -e

urls_py="work/myproject/urls.py"
target="from django.urls import path, include"

# include を追加
if ! grep -q "$target" "$urls_py"; then
    sed -i "s/from django.urls import path/$target/" "$urls_py"
fi

# api/ を追加
if ! grep -q "path('api/', include('myapp.urls_api'))" "$urls_py"; then
    sed -i "/^]/i\    path('api/', include('myapp.urls_api'))," "$urls_py"
fi

