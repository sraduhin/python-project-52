from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from task_manager.users.utils import (CustomUnAuthorizedMixin,
                                      PrettyBusinessObjectMixin)

SUCCESS_CREATE_MESSAGE = _("Status successfully created")
SUCCESS_UPDATE_MESSAGE = _("Status successfully updated")
SUCCESS_DELETE_MESSAGE = _("Status successfully deleted")
ERROR_DELETE_MESSAGE = _("Can't remove the status because it's in use")


class StatusesListView(CustomUnAuthorizedMixin, ListView):
    model = Status

    template_name = 'statuses/index.html'


class StatusesCreateView(CustomUnAuthorizedMixin, CreateView):
    form_class = StatusForm
    success_message = SUCCESS_CREATE_MESSAGE
    success_url = reverse_lazy('statuses_index')
    template_name = 'statuses/create.html'


class StatusesUpdateView(CustomUnAuthorizedMixin, UpdateView):
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses_index')
    template_name = 'statuses/update.html'
    success_message = SUCCESS_UPDATE_MESSAGE


class StatusesDeleteView(CustomUnAuthorizedMixin,
                         PrettyBusinessObjectMixin,
                         DeleteView):
    model = Status
    success_url = reverse_lazy('statuses_index')
    template_name = 'statuses/delete.html'
    success_message = SUCCESS_DELETE_MESSAGE

    fail_url = 'statuses_index'
    error_delete_message = ERROR_DELETE_MESSAGE
