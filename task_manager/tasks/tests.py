from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.tasks.models import Task
from task_manager.utils import get_test_data


class AppTaskTest(TestCase):

    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.auth_user = Client()
        self.auth_user.force_login(self.user)

    def test_CreateTask(self):
        TASK = get_test_data('tasks', 'new')

        response = self.auth_user.post(reverse('tasks_create'), TASK)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_index'))
        response = self.auth_user.get(reverse('tasks_index'))
        self.assertContains(response, TASK['name'])

    def test_UpdateTask(self):
        CHANGES = get_test_data('tasks', 'changed')

        task = Task.objects.last()
        response = self.auth_user.post(
            reverse('tasks_update', kwargs={'pk': task.id}), CHANGES
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_index'))

        response = self.auth_user.get(reverse('tasks_index'))
        self.assertContains(response, CHANGES['name'])

    def test_DeleteTask(self):
        response = self.auth_user.post(
            reverse('tasks_delete', kwargs={'pk': 999})  # non-existent
        )
        self.assertEqual(response.status_code, 404)

        task = Task.objects.last()
        response = self.auth_user.post(
            reverse('tasks_delete', kwargs={'pk': task.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_index'))

        response = self.auth_user.get(reverse('tasks_index'))
        self.assertNotContains(response, task.__str__)
