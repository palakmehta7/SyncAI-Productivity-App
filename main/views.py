from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Project, Asignee
from main.lib import process_prs

def project_dashboard(request):
    projects = Project.objects.prefetch_related('task_set')
    assignees = Asignee.objects.all()
    return render(request, 'project_dashboard.html', {'projects': projects, 'assignees': assignees})


from django.shortcuts import render, redirect
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
