from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.shortcuts import redirect

ERROR_AUTH_MESSAGE = "Вы не авторизованы! Пожалуйста, выполните вход."
ERROR_UPDATE_MESSAGE = "У вас нет прав для изменения другого пользователя."


class CustomPermissionRequiredMixin(SuccessMessageMixin, LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, ERROR_AUTH_MESSAGE
            )
            return redirect('login')

        elif self.request.user != self.get_object():
            messages.error(
                request, ERROR_UPDATE_MESSAGE
            )
            return redirect('users_index')
        return super().dispatch(request, *args, **kwargs)