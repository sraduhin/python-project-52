from task_manager.utils import CustomUnAuthorizedMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.tasks.filters import TaskFilter
from django_filters.views import FilterView

SUCCESS_CREATE_MESSAGE = "Задача успешно создана"
SUCCESS_UPDATE_MESSAGE = "Задача успешно изменена"
SUCCESS_DELETE_MESSAGE = "Задача успешно удалена"


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


class TasksDeleteView(CustomUnAuthorizedMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks_index')
    template_name = 'tasks/delete.html'
    success_message = SUCCESS_DELETE_MESSAGE
