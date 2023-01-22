from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.labels.models import Label

AUTH_USERNAME = {
        'first_name': 'Имечко',
        'last_name': 'Фамилия',
        'username': 'IAmIsAuthorizated',
        'password1': '123',
        'password2': '123',
    }
LABEL = {'name': 'label'}
LABEL_CHANGED = {'name': 'changed'}


class AppLabelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username=AUTH_USERNAME['username']
        )
        self.auth_user = Client()
        self.auth_user.force_login(self.user)

    def test_CreateLabel(self):
        response = self.auth_user.post(reverse('labels_create'), LABEL)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_index'))
        response = self.auth_user.get(reverse('labels_index'))
        self.assertContains(response, LABEL['name'])

    def test_UpdateLabel(self):
        response = self.auth_user.post(reverse('labels_create'), LABEL)

        label = Label.objects.last()
        response = self.auth_user.post(
            reverse('labels_update', kwargs={'pk': label.id}), LABEL_CHANGED
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_index'))

        response = self.auth_user.get(reverse('labels_index'))
        self.assertContains(response, LABEL_CHANGED['name'])

    def test_DeleteLabel(self):
        response = self.auth_user.post(reverse('labels_create'), LABEL)

        label = Label.objects.last()
        response = self.auth_user.post(
            reverse('labels_delete', kwargs={'pk': label.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_index'))

        response = self.auth_user.get(reverse('labels_index'))
        self.assertFalse(Label.objects.filter(name=LABEL['name']))
