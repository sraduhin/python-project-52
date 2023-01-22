from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.statuses.models import Status

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
    def setUp(self):
        self.user = get_user_model().objects.create(
            username=AUTH_USERNAME['username']
        )
        self.auth_user = Client()
        self.auth_user.force_login(self.user)

    def test_CreateStatus(self):
        response = self.auth_user.post(reverse('statuses_create'), STATUS)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_index'))
        response = self.auth_user.get(reverse('statuses_index'))
        self.assertContains(response, STATUS['name'])

    def test_UpdateStatus(self):
        response = self.auth_user.post(reverse('statuses_create'), STATUS)

        status = Status.objects.last()
        response = self.auth_user.post(
            reverse(
                'statuses_update', kwargs={'pk': status.id}
                ), STATUS_CHANGED
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_index'))

        response = self.auth_user.get(reverse('statuses_index'))
        self.assertContains(response, STATUS_CHANGED['name'])

    def test_DeleteStatus(self):
        response = self.auth_user.post(reverse('statuses_create'), STATUS)

        status = Status.objects.last()
        response = self.auth_user.post(
            reverse('statuses_delete', kwargs={'pk': status.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_index'))

        response = self.auth_user.get(reverse('statuses_index'))
        self.assertFalse(Status.objects.filter(name=STATUS['name']))
