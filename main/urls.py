# yourapp/urls.py
from django.urls import path
from .views import project_dashboard


urlpatterns = [
    path('projects/', project_dashboard, name='project_dashboard')
]
