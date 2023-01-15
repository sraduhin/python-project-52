from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import gettext as _

SUCCESS_LOGIN_MESSAGE = _("You are logged in")
SUCCESS_LOGOUT_MESSAGE = _("You are logged out")


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_message = SUCCESS_LOGIN_MESSAGE


class CustomLogoutView(LogoutView):
    success_message = SUCCESS_LOGOUT_MESSAGE

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, SUCCESS_LOGOUT_MESSAGE)
        return response
