from django_filters.views import FilterView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from task_manager.mixins import (CustomUnAuthorizedMixin,
                                 PrettyBusinessTaskMixin)
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task

SUCCESS_CREATE_MESSAGE = _("Task successfully created")
SUCCESS_UPDATE_MESSAGE = _("Task successfully updated")
SUCCESS_DELETE_MESSAGE = _("Task successfully deleted")
ERROR_DELETE_MESSAGE = _("A task can only be deleted by its author")


class TasksListView(CustomUnAuthorizedMixin, FilterView):
    model = Task
    login_url = 'login'
    template_name = 'tasks/index.html'
    filterset_class = TaskFilter


class TasksCreateView(CustomUnAuthorizedMixin, CreateView):
    form_class = TaskForm
    success_message = SUCCESS_CREATE_MESSAGE
    success_url = reverse_lazy('tasks_index')
    template_name = 'tasks/create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TasksDetailView(CustomUnAuthorizedMixin, DetailView):
    model = Task
    template_name = 'tasks/show.html'


class TasksUpdateView(CustomUnAuthorizedMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks_index')
    template_name = 'tasks/update.html'
    success_message = SUCCESS_UPDATE_MESSAGE


class TasksDeleteView(CustomUnAuthorizedMixin,
                      PrettyBusinessTaskMixin,
                      DeleteView):
    model = Task
    success_url = reverse_lazy('tasks_index')
    template_name = 'tasks/delete.html'
    success_message = SUCCESS_DELETE_MESSAGE

    fail_url = 'tasks_index'
    error_delete_message = ERROR_DELETE_MESSAGE
