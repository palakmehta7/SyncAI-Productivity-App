# yourapp/urls.py
from django.urls import path
from .views import project_dashboard, delete_task, sync_tasks, get_pr_summary


urlpatterns = [
    path('projects/', project_dashboard, name='project_dashboard'),
    path('task/delete/<int:task_id>/', delete_task, name='delete_task'),
    path('sync-tasks/', sync_tasks, name='sync_tasks'),
    path("get_pr_summary/", get_pr_summary, name="get_pr_summary"),
]
