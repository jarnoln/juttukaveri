import json

from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from api01.models import Session, Transcript, Reply


class StartSessionViewTests(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse("start_session"), "/api01/start_session")

    def test_get_session_id(self):
        url = reverse("start_session")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out["id"]), 43)


class SessionListViewTests(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse("session_list"), "/api01/sessions")

    def test_get_sessions(self):
        url = reverse("session_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 0)
        session_1 = Session.objects.create(session_id="abc")
        Transcript.objects.create(session=session_1, text="trancript1")
        Reply.objects.create(session=session_1, text="reply1")
        response = self.client.get(url)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 1)
        self.assertEqual(data_out[0]["session_id"], "abc")
        self.assertEqual(len(data_out[0]["transcripts"]), 1)
        self.assertEqual(len(data_out[0]["replies"]), 1)


class AboutViewTests(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse("about"), "/api01/about")

    def test_get_about_content(self):
        url = reverse("about")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertTrue(len(data_out["readme"]) > 2000)
