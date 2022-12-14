from django.test import TestCase

from books.models import Book, BookReview
from users.models import CustomUser
from django.urls import reverse


class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="15235235")
        user = CustomUser.objects.create(
            username="abbos", first_name="Abbos", last_name="Isagaliyev", email="abboscode@gmail.com"
        )
        user.set_password("abbos1234")
        user.save()
        review1 = BookReview.objects.create(book=book, user=user, stars_given=3, comment="Very good book")
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment="Useful book")
        review3 = BookReview.objects.create(book=book, user=user, stars_given=5, comment="Nice book")

        response = self.client.get(reverse("home_page") + "?page_size=2")

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)