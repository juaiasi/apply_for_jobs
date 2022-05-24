from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_sharer, name='create_sharer'),
    path('userlink/<int:user>',views.display_link, name='display_link'),
    path('S<slug:code>', views.sharer, name='sharer')
]