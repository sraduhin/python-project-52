from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from task_manager.forms import SignUpForm
from task_manager.mixins import CustomPermissionRequiredMixin
from task_manager.mixins import CustomUnAuthorizedMixin
from task_manager.mixins import PrettyBusinessUserMixin

SUCCESS_REGISTRATION_MESSAGE = _("Successfull sign up")
SUCCESS_UPDATE_MESSAGE = _("User successfully updated")
SUCCESS_DELETE_MESSAGE = _("User successfully deleted")


class UsersListView(ListView):
    # paginate_by = 10
    model = get_user_model()

    template_name = 'users/index.html'


class UsersSignUpView(SuccessMessageMixin, CreateView):
    form_class = SignUpForm
    success_message = SUCCESS_REGISTRATION_MESSAGE
    success_url = reverse_lazy('login')
    template_name = 'users/create.html'


class UsersUpdateView(CustomUnAuthorizedMixin, CustomPermissionRequiredMixin,
                      UpdateView):
    model = get_user_model()
    form_class = SignUpForm
    success_url = reverse_lazy('users_index')
    template_name = 'users/update.html'
    success_message = SUCCESS_UPDATE_MESSAGE


class UsersDeleteView(CustomUnAuthorizedMixin,
                      CustomPermissionRequiredMixin,
                      PrettyBusinessUserMixin,
                      DeleteView):
    model = get_user_model()
    success_url = reverse_lazy('users_index')
    template_name = 'users/delete.html'
    success_message = SUCCESS_DELETE_MESSAGE
