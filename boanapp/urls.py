from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-data/', views.get_data, name='get_data'),
    path('visualize-data/', views.visualize_data, name='visualize_data')
]
