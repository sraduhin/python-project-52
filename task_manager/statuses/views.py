from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status

SUCCESS_CREATE_MESSAGE = "Статус успешно создан"
SUCCESS_UPDATE_MESSAGE = "Статус успешно изменён"
SUCCESS_DELETE_MESSAGE = "Статус успешно удалён"


class StatusesListView(ListView):
    model = Status

    template_name = 'statuses/index.html'


class StatusesCreateView(SuccessMessageMixin, CreateView):
    form_class = StatusForm
    success_message = SUCCESS_CREATE_MESSAGE
    success_url = reverse_lazy('statuses_index')
    template_name = 'statuses/create.html'


class StatusesUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses_index')
    template_name = 'statuses/update.html'
    success_message = SUCCESS_UPDATE_MESSAGE


class StatusesDeleteView(DeleteView):
    model = Status
    success_url = reverse_lazy('statuses_index')
    template_name = 'statuses/delete.html'
    success_message = SUCCESS_DELETE_MESSAGE
