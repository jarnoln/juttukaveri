from django.test import TestCase
from django.urls import reverse

from rest_framework import status


class SessionViewTests(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse("start_session"), "/api01/start_session")

    def test_get_session_id(self):
        url = reverse("start_session")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.content), 45)
