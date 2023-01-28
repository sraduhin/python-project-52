from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.labels.models import Label
from task_manager.utils import get_test_data


class AppLabelTest(TestCase):

    fixtures = ['users.json', 'labels.json']

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.auth_user = Client()
        self.auth_user.force_login(self.user)

    def test_CreateLabel(self):
        NEW_LABEL = get_test_data('labels', 'new')
        EXISTS_LABEL = get_test_data('labels', 'exists')

        response = self.auth_user.post(reverse('labels_create'), EXISTS_LABEL)
        self.assertEqual(response.status_code, 200)

        response = self.auth_user.post(reverse('labels_create'), NEW_LABEL)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_index'))
        response = self.auth_user.get(reverse('labels_index'))
        self.assertContains(response, NEW_LABEL['name'])

    def test_UpdateLabel(self):
        GHANGES = get_test_data('labels', 'changed')

        label = Label.objects.last()
        response = self.auth_user.post(
            reverse('labels_update', kwargs={'pk': label.id}), GHANGES
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_index'))

        response = self.auth_user.get(reverse('labels_index'))
        self.assertContains(response, GHANGES['name'])

    def test_DeleteLabel(self):
        response = self.auth_user.post(
            reverse('labels_delete', kwargs={'pk': 999})  # non-existent
        )

        self.assertEqual(response.status_code, 404)
        label = Label.objects.last()
        response = self.auth_user.post(
            reverse('labels_delete', kwargs={'pk': label.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_index'))

        response = self.auth_user.get(reverse('labels_index'))
        self.assertNotContains(response, label.__str__)
