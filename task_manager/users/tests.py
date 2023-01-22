from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

AUTH_USERNAME = {
        'first_name': 'Имечко',
        'last_name': 'Фамилия',
        'username': 'IAmIsAuthorizated',
        'password1': '123',
        'password2': '123',
    }
NEW_USER = {
        'first_name': 'My',
        'last_name': 'NameIs',
        'username': 'SlimShady',
        'password1': 'stan',
        'password2': 'stan',
    }


class AppUserTest(TestCase):
    def setUp(self):
        self.guest = Client()
        self.user = get_user_model().objects.create(
            username=AUTH_USERNAME['username']
        )
        self.auth_user = Client()
        self.auth_user.force_login(self.user)

    def test_SignUp(self):
        response = self.guest.get(reverse('users_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/create.html')

        response = self.guest.post(reverse('users_create'), NEW_USER)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        new_user = get_user_model().objects.last()
        self.assertEqual(
            new_user.__str__(), f"{NEW_USER['first_name']} {NEW_USER['last_name']}"
        )
        self.assertEqual(new_user.first_name, NEW_USER['first_name'])
        self.assertEqual(new_user.last_name, NEW_USER['last_name'])
        self.assertEqual(new_user.username, NEW_USER['username'])

        response = self.client.get(reverse('users_index'))
        self.assertContains(response, new_user.username)

    def test_UpdateUser(self):
        user = get_user_model().objects.first()
        response = self.guest.get(
            reverse('users_update', kwargs={'pk': user.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        user = get_user_model().objects.get(username=AUTH_USERNAME['username'])
        response = self.auth_user.get(
            reverse('users_update', kwargs={'pk': user.id})
        )
        self.assertEqual(response.status_code, 200)
        response = self.auth_user.post(
            reverse('users_update', kwargs={'pk': user.id}), AUTH_USERNAME
        )
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.first_name, AUTH_USERNAME['first_name'])

    def test_DeleteUser(self):
        user = get_user_model().objects.first()
        response = self.guest.get(
            reverse('users_delete', kwargs={'pk': user.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        self.assertEqual(user.username, AUTH_USERNAME['username'])
        user = get_user_model().objects.get(username=AUTH_USERNAME['username'])
        response = self.auth_user.post(
            reverse('users_delete', kwargs={'pk': user.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_index'))
        self.assertFalse(get_user_model().objects.filter(username=AUTH_USERNAME['username']))
