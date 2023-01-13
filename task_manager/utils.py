from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _

from django.contrib import messages
from django.shortcuts import redirect

ERROR_AUTH_MESSAGE = _("Unauthorized! Sign in please.")
#ERROR_AUTH_MESSAGE = "Вы не авторизованы! Пожалуйста, выполните вход."
ERROR_UPDATE_MESSAGE = "You don't have permission to edit other user."
#ERROR_UPDATE_MESSAGE = "У вас нет прав для изменения другого пользователя."


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