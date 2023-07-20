from django.test import TestCase
from api01.models import Session


class SessionModelTests(TestCase):
    def test_can_save_and_load(self):
        session = Session()
        session.save()
        self.assertEqual(Session.objects.count(), 1)
        self.assertEqual(Session.objects.first(), session)

    def test_string(self):
        session = Session.objects.create(session_id='abc')
        session_str = str(session)
        self.assertTrue(session_str.startswith('abc:'))
