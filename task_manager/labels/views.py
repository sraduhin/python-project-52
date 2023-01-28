from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.users.utils import (CustomUnAuthorizedMixin,
                                      PrettyBusinessObjectMixin)

SUCCESS_CREATE_MESSAGE = _("Label successfully created")
SUCCESS_UPDATE_MESSAGE = _("Label successfully updated")
SUCCESS_DELETE_MESSAGE = _("Label successfully deleted")
ERROR_DELETE_MESSAGE = _("Can't remove the label because it's in use")


class LabelsListView(CustomUnAuthorizedMixin, ListView):
    model = Label

    template_name = 'labels/index.html'


class LabelsCreateView(CustomUnAuthorizedMixin, CreateView):
    form_class = LabelForm
    success_message = SUCCESS_CREATE_MESSAGE
    success_url = reverse_lazy('labels_index')
    template_name = 'labels/create.html'


class LabelsUpdateView(CustomUnAuthorizedMixin, UpdateView):
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy('labels_index')
    template_name = 'labels/update.html'
    success_message = SUCCESS_UPDATE_MESSAGE


class LabelsDeleteView(CustomUnAuthorizedMixin,
                       PrettyBusinessObjectMixin,
                       DeleteView):
    model = Label
    success_url = reverse_lazy('labels_index')
    template_name = 'labels/delete.html'
    success_message = SUCCESS_DELETE_MESSAGE

    error_delete_message = ERROR_DELETE_MESSAGE
    fail_url = 'labels_index'
