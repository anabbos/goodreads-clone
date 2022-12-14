from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser

class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
                        reverse("users:register"),
                         data={
                             "username": "abbos",
                             "first_name": "Abbos",
                             "last_name": "Isagaliyev",
                             "email": "abboscode@gmail.com",
                             "password": "abbos1234"
                         }
        )

        user = CustomUser.objects.get(username="abbos")

        self.assertEqual(user.first_name, "Abbos")
        self.assertEqual(user.last_name, "Isagaliyev")
        self.assertEqual(user.email, "abboscode@gmail.com")
        self.assertNotEqual(user.password, "abbos1234")
        self.assertTrue(user.check_password("abbos1234"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "Abbos",
                "email": "abboscode@gmail.com"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "abbos",
                "first_name": "Abbos",
                "last_name": "Isagaliyev",
                "email": "invalid_email",
                "password": "abbos1234"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        user = CustomUser.objects.create(username="abbos", first_name="Abbos")
        user.set_password("abbos1234")
        user.save()

        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "abbos",
                "first_name": "Abbos",
                "last_name": "Isagaliyev",
                "email": "abboscode@gmail.com",
                "password": "abbos1234"
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, "form", "username", "A user with that username already exists.")

class LoginTestCase(TestCase):
    def setUp(self):
        db_user = CustomUser.objects.create(username="abbos", first_name="Abbos")
        db_user.set_password("abbos1234")
        db_user.save()


    def test_successful_login(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "abbos",
                "password": "abbos1234"
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong-username",
                "password": "abbos1234"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("users:login"),
            data={
                "username": "abbos",
                "password": "wrong-password"
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username="abbos", password="abbos1234")

        self.client.get(reverse("users:logout"))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username="abbos",
            first_name="Abbos",
            last_name="Isagaliyev",
            email="abbos@gmail.com"
        )
        user.set_password("abbos1234")
        user.save()

        self.client.login(username="abbos", password="abbos1234")

        response = self.client.get(reverse("users:profile"))


        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username="abbos", first_name="Abbos", last_name="Isagaliyev", email="abbos@gmail.com"
        )
        user.set_password("abbos1234")
        user.save()

        self.client.login(username="abbos", password="abbos1234")

        response = self.client.post(
            reverse("users:profile-edit"),
            data={
                "username": "abbos",
                "first_name": "Abbos",
                "last_name": "Rahmonov",
                "email": "abboscode@gmail.com"
            }
        )
        user.refresh_from_db()

        self.assertEqual(user.last_name, "Rahmonov")
        self.assertEqual(user.email, "abboscode@gmail.com")
        self.assertEqual(response.url, reverse("users:profile"))






