from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


ERROR_AUTH_MESSAGE = _("Unauthorized! Sign in please.")
ERROR_UPDATE_MESSAGE = _("You don't have permission to edit other user.")
ERROR_DELETE_MESSAGE = _("Cannot delete user because it is in use")


class CustomUnAuthorizedMixin(LoginRequiredMixin, SuccessMessageMixin):

    def handle_no_permission(self):
        messages.error(self.request, ERROR_AUTH_MESSAGE)
        return redirect(reverse_lazy('login'))


class CustomPermissionRequiredMixin():

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object():
            messages.error(
                request, ERROR_UPDATE_MESSAGE
            )
            return redirect(reverse_lazy('users_index'))
        return super().dispatch(request, *args, **kwargs)


class PrettyBusinessUserMixin():

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner.first() or obj.executor.first():
            messages.error(
                request, ERROR_DELETE_MESSAGE
            )
            return redirect(reverse_lazy('users_index'))
        return super().dispatch(request, *args, **kwargs)


class PrettyBusinessObjectMixin(LoginRequiredMixin):
    error_delete_message = ''
    fail_url = ''

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and self.get_object().task_set.first():  # noqa E501
            messages.error(
                request, self.error_delete_message
            )
            return redirect(reverse_lazy(self.fail_url))
        return super().dispatch(request, *args, **kwargs)
