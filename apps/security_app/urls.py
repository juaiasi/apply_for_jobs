from django.urls import path
from . import views

urlpatterns = [
    path('',views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('createsharer', views.create_sharer, name='create_sharer'),
    path('userlink/<int:user>',views.display_link, name='display_link'),
    path('S<slug:code>', views.sharer, name='sharer'),
    path('logged',views.logged, name='logged')
]