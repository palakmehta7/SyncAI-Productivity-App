from django import forms
from .models import Task, Asignee

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['desc', 'asignee']  # Include 'asignee' for the dropdown
