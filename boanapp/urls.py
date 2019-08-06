from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.visualize_data, name='index'),
    path('get-data/', views.get_data, name='get_data'),
    path('visualize-data/', views.visualize_data, name='visualize_data'),
    path('visualize-specified-data/',
         views.visulize_defined_data, name='visulize_defined_data')
]
