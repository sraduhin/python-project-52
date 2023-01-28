from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AppTest(TestCase):

    fixtures = ['users.json']

    def setUp(self):
        self.guest = Client()

        self.user = get_user_model().objects.get(pk=1)
        self.auth_user = Client()
        self.auth_user.force_login(self.user)

    def test_index_page(self):
        response = self.guest.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='index.html')

    def test_users_page(self):
        response = self.guest.get(reverse('users_index'))
        self.assertTemplateUsed(response, template_name='users/index.html')
        self.assertEqual(response.status_code, 200)

    def test_labels_page(self):
        response = self.auth_user.get(reverse('labels_index'))
        self.assertEqual(response.status_code, 200)
        response = self.guest.get(reverse('labels_index'))
        self.assertEqual(response.status_code, 302)

    def test_task_page(self):
        response = self.auth_user.get(reverse('tasks_index'))
        self.assertEqual(response.status_code, 200)
        response = self.guest.get(reverse('tasks_index'))
        self.assertEqual(response.status_code, 302)
