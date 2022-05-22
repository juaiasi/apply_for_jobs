from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_sharer, name='create_sharer'),
    path('share', views.sharer, name='sharer')
]