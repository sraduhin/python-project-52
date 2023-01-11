import django_filters
from django import forms
from task_manager.tasks.models import Task
from task_manager.labels.models import Label


class TaskFilter(django_filters.FilterSet):
    def get_self_tasks(self, queryset, *args):
        return queryset.filter(owner=self.request.user)


    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all()
    )

    self_tasks = django_filters.BooleanFilter(
        widget=forms.CheckboxInput(),
        method='get_self_tasks',
        label='Только свои задачи'
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']