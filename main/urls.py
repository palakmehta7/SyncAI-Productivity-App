# yourapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.project_dashboard, name='project_dashboard'),
    path("get_pr_summary/", views.my_view, name="get_pr_summary_view"),
]
