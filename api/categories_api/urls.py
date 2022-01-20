from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [
        
    # endpoint
    path('top', views.get_top_categories),
    path('', views.get_all_categories),
    
]
