from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from main.lib import process_prs
from .models import Project, Asignee, Task
from django.shortcuts import redirect, get_object_or_404

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
