from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.tasks.models import Task

AUTH_USERNAME = {
    'first_name': 'Имечко',
    'last_name': 'Фамилия',
    'username': 'IAmIsAuthorizated',
    'password1': '123',
    'password2': '123',
}
STATUS = {'name': 'name'}
TASK = {
    'name': 'task',
    'description': 'description',
    'owner': 1,
    'status': 1,
    # 'executor': 'executor',
    # 'labels': 'labels',
    }

TASK_CHANGED = {
    'name': 'changed',
    'description': 'changed',
    'owner': 1,
    'status': 1,
    # 'executor': 'executor',
    # 'labels': 'labels',
    }


class AppTaskTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username=AUTH_USERNAME['username']
        )
        self.auth_user = Client()
        self.auth_user.force_login(self.user)
        self.auth_user.post(reverse('statuses_create'), STATUS)

    def test_CreateTask(self):
        response = self.auth_user.post(reverse('tasks_create'), TASK)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_index'))
        response = self.auth_user.get(reverse('tasks_index'))
        self.assertContains(response, TASK['name'])

    def test_UpdateTask(self):
        response = self.auth_user.post(reverse('tasks_create'), TASK)

        task = Task.objects.last()
        response = self.auth_user.post(
            reverse(
                'tasks_update', kwargs={'pk': task.id}
                ), TASK_CHANGED
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_index'))

        response = self.auth_user.get(reverse('tasks_index'))
        self.assertContains(response, TASK_CHANGED['name'])

    def test_DeleteTask(self):
        response = self.auth_user.post(reverse('tasks_create'), TASK)

        task = Task.objects.last()
        response = self.auth_user.post(
            reverse('tasks_delete', kwargs={'pk': task.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_index'))

        response = self.auth_user.get(reverse('tasks_index'))
        self.assertFalse(Task.objects.filter(name=TASK['name']))
