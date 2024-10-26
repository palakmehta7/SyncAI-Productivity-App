
from datetime import datetime
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Project, Asignee, Task, Board, STATUSES
from main.lib import process_prs
from django.shortcuts import redirect, get_object_or_404
from .gpt_helper import get_paginated_diffs

def project_dashboard(request):
    projects = Project.objects.prefetch_related('task_set')
    assignees = Asignee.objects.all()
    return render(request, 'project_dashboard.html', {'projects': projects, 'assignees': assignees})


from django.shortcuts import render, redirect, get_object_or_404

from .models import Project
from .forms import TaskForm

def project_dashboard(request):
    projects = Project.objects.prefetch_related('task_set__asignee').all()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()  # Save the task with the selected asignee
            return redirect('project_dashboard')  # Redirect to avoid duplicate submissions
    else:
        form = TaskForm()

    return render(request, 'project_dashboard.html', {'projects': projects, 'form': form})


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})


def get_pr_summary(request):
    projects = Project.objects.prefetch_related('task_set__asignee').all()
    print(f"\n debug_logs - 33 - projects = {projects}")

    is_process_success = process_prs(projects)
    resp = {'is_process_success': is_process_success}
    print(f"\n debug_logs - 8 - resp = {resp}")
    return JsonResponse(resp)


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_deleted = True  # Mark the task as deleted
    task.save()
    return redirect('project_dashboard')  # Replace with your view name


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Disable CSRF validation for this view, use cautiously!
def sync_tasks(request):
    if request.method == "POST":
        # Your logic to sync tasks with GitHub here
        # e.g., fetch PRs, update task statuses
        projects = Project.objects.prefetch_related('task_set__asignee').all()
        print(f"\n debug_logs - 33 - projects = {projects}")

        is_process_success = process_prs(projects)
        resp = {'is_process_success': is_process_success}
        print(f"\n debug_logs - 8 - resp = {resp}")
        tasks = Task.objects.filter(pr_id__isnull=False)
        for task in tasks:
            task_completion_response = get_paginated_diffs(task, task_desc=task.desc)
            precentage_done, precentage_pending = task_completion_response
            task.progress = float(precentage_done)
            if float(precentage_done) > 0:
                task.status = STATUSES[1][0]  #IN_PROGRESS
            if precentage_pending == '0':
                task.status = STATUSES[2][0]  #DONE
            task.save()
        # Mock response (replace with actual data handling logic)
        return JsonResponse({"status": "success", "message": "Tasks synced successfully."})

    return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)
