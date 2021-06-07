"""
Definition of urls for Praktika.
"""

from datetime import datetime
from django.urls import path
from app import forms, views


urlpatterns = [
    path('', views.Home, name='home'),
    path('work/', views.Workers, name='work'),
    path('work/create/', views.create),
	path('works/', views.Works, name='works')
]