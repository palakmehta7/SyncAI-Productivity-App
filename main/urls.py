# yourapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.project_dashboard, name='project_dashboard'),
    path("get_pr_summary/", views.get_pr_summary, name="get_pr_summary"),
]
