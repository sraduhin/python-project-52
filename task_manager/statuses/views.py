from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from django.utils.translation import gettext as _

from django.contrib import messages
from django.shortcuts import redirect

SUCCESS_CREATE_MESSAGE = _("Status successfully created")
SUCCESS_UPDATE_MESSAGE = _("Status successfully updated")
SUCCESS_DELETE_MESSAGE = _("Status successfully deleted")
ERROR_DELETE_MESSAGE = _("Can't remove the status because it's in use")


class StatusesListView(LoginRequiredMixin, ListView):
    model = Status

    template_name = 'statuses/index.html'


class StatusesCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = StatusForm
    success_message = SUCCESS_CREATE_MESSAGE
    success_url = reverse_lazy('statuses_index')
    template_name = 'statuses/create.html'


class StatusesUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses_index')
    template_name = 'statuses/update.html'
    success_message = SUCCESS_UPDATE_MESSAGE


class StatusesDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    success_url = reverse_lazy('statuses_index')
    template_name = 'statuses/delete.html'
    success_message = SUCCESS_DELETE_MESSAGE

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().task_set.first():
            messages.error(
                request, ERROR_DELETE_MESSAGE
            )
            return redirect('statuses_index')
        return super().dispatch(request, *args, **kwargs)
