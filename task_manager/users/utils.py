from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import gettext as _


ERROR_AUTH_MESSAGE = _("Unauthorized! Sign in please.")
ERROR_UPDATE_MESSAGE = _("You don't have permission to edit other user.")
ERROR_DELETE_MESSAGE = _("Cannot delete user because it is in use")


class CustomUnAuthorizedMixin(SuccessMessageMixin, LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, ERROR_AUTH_MESSAGE
            )
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class CustomPermissionRequiredMixin(SuccessMessageMixin, LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object():
            messages.error(
                request, ERROR_UPDATE_MESSAGE
            )
            return redirect('users_index')
        return super().dispatch(request, *args, **kwargs)


class PrettyBusinessUserMixin():

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner.first() or obj.executor.first():
            messages.error(
                request, ERROR_DELETE_MESSAGE
            )
            return redirect('users_index')
        return super().dispatch(request, *args, **kwargs)
