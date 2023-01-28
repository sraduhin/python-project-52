from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.utils import get_test_data


class AppUserTest(TestCase):

    fixtures = ['users.json']

    def setUp(self):
        self.guest = Client()

        self.user = get_user_model().objects.get(pk=1)
        self.auth_user = Client()
        self.auth_user.force_login(self.user)

    def test_sign_up(self):
        NEW_USER = get_test_data('users', 'new')

        response = self.guest.get(reverse('users_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/create.html')

        response = self.guest.post(reverse('users_create'), NEW_USER)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        new_user = get_user_model().objects.last()
        self.assertEqual(
            new_user.__str__(),
            f"{NEW_USER['first_name']} {NEW_USER['last_name']}"
        )
        self.assertEqual(new_user.first_name, NEW_USER['first_name'])
        self.assertEqual(new_user.last_name, NEW_USER['last_name'])
        self.assertEqual(new_user.username, NEW_USER['username'])

        response = self.client.get(reverse('users_index'))
        self.assertContains(response, new_user.username)

    def test_update_user(self):
        CHANGES = get_test_data('users', 'changed')

        user = get_user_model().objects.first()
        response = self.guest.get(
            reverse('users_update', kwargs={'pk': user.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        user = get_user_model().objects.get(pk=1)
        response = self.auth_user.get(
            reverse('users_update', kwargs={'pk': user.id})
        )
        self.assertEqual(response.status_code, 200)
        response = self.auth_user.post(
            reverse('users_update', kwargs={'pk': user.id}), CHANGES
        )
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.last_name, CHANGES['last_name'])

    def test_delete_user(self):
        user = get_user_model().objects.first()
        response = self.guest.get(
            reverse('users_delete', kwargs={'pk': user.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        user = get_user_model().objects.get(pk=1)
        response = self.auth_user.post(
            reverse('users_delete', kwargs={'pk': user.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_index'))
        self.assertFalse(
            get_user_model().objects.filter(pk=1)
        )
