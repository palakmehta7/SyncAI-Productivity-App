# yourapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.project_dashboard, name='project_dashboard'),
]
