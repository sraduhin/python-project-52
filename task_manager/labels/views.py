from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from django.utils.translation import gettext as _

from django.contrib import messages
from django.shortcuts import redirect

SUCCESS_CREATE_MESSAGE = _("Label successfully created")
SUCCESS_UPDATE_MESSAGE = _("Label successfully updated")
SUCCESS_DELETE_MESSAGE = _("Label successfully deleted")
ERROR_DELETE_MESSAGE = _("Can't remove the label because it's in use")


class LabelsListView(LoginRequiredMixin, ListView):
    model = Label

    template_name = 'labels/index.html'


class LabelsCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = LabelForm
    success_message = SUCCESS_CREATE_MESSAGE
    success_url = reverse_lazy('labels_index')
    template_name = 'labels/create.html'


class LabelsUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy('labels_index')
    template_name = 'labels/update.html'
    success_message = SUCCESS_UPDATE_MESSAGE


class LabelsDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    success_url = reverse_lazy('labels_index')
    template_name = 'labels/delete.html'
    success_message = SUCCESS_DELETE_MESSAGE

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().task_set.first():
            messages.error(
                request, ERROR_DELETE_MESSAGE
            )
            return redirect('labels_index')
        return super().dispatch(request, *args, **kwargs)
