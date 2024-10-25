from django.contrib import admin
from .models import Project, Task, Asignee

# Project Model
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'desc', 'created_at', 'updated_at', 'summary', 'progress')

    def __str__(self):
        return f"{self.desc} - {self.progress}%"  # Customize Project's display name


# Task Model
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'desc', 'project', 'asignee', 'created_at', 'updated_at', 'status', 'summary', 'progress')

    def __str__(self):
        return f"{self.desc} - {self.status} - {self.progress}%"  # Customize Task's display name


# Asignee Model
class AsigneeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at', 'manager')

    def __str__(self):
        return self.name  # Customize Asignee's display name


# Register the models with Django Admin
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Asignee, AsigneeAdmin)
