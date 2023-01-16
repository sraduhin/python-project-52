from django import forms
from task_manager.tasks.models import Task
from task_manager.users.models import CustomUser


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
