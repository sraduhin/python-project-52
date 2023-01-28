from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.statuses.models import Status
from task_manager.utils import get_test_data

AUTH_USERNAME = {
    'first_name': 'Имечко',
    'last_name': 'Фамилия',
    'username': 'IAmIsAuthorizated',
    'password1': '123',
    'password2': '123',
}
STATUS = {'name': 'status'}
STATUS_CHANGED = {'name': 'changed'}


class AppStatusTest(TestCase):

    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.auth_user = Client()
        self.auth_user.force_login(self.user)

    def test_CreateStatus(self):
        NEW_STATUS = get_test_data('statuses', 'new')
        EXISTS_STATUS = get_test_data('statuses', 'exists')

        response = self.auth_user.post(
            reverse('statuses_create'), EXISTS_STATUS
        )
        self.assertEqual(response.status_code, 200)

        response = self.auth_user.post(reverse('statuses_create'), NEW_STATUS)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_index'))
        response = self.auth_user.get(reverse('statuses_index'))
        self.assertContains(response, NEW_STATUS['name'])

    def test_UpdateStatus(self):
        CHANGES = get_test_data('labels', 'changed')

        status = Status.objects.last()
        response = self.auth_user.post(
            reverse('statuses_update', kwargs={'pk': status.id}), CHANGES
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_index'))

        response = self.auth_user.get(reverse('statuses_index'))
        self.assertContains(response, CHANGES['name'])

    def test_DeleteStatus(self):
        response = self.auth_user.post(
            reverse('statuses_delete', kwargs={'pk': 999})  # non-existent
        )
        self.assertEqual(response.status_code, 404)

        status = Status.objects.last()
        response = self.auth_user.post(
            reverse('statuses_delete', kwargs={'pk': status.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_index'))

        response = self.auth_user.get(reverse('statuses_index'))
        self.assertNotContains(response, status.__str__)
