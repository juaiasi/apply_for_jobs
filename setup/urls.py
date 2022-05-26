"""setup URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',include('security_app.urls')),
    path('admin/', admin.site.urls)
]
