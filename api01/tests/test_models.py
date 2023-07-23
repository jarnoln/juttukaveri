from django.test import TestCase
from api01.models import Session, Transcript, Reply


class SessionModelTests(TestCase):
    def test_can_save_and_load(self):
        session = Session()
        session.save()
        self.assertEqual(Session.objects.count(), 1)
        self.assertEqual(Session.objects.first(), session)

    def test_string(self):
        session = Session.objects.create(session_id="abc")
        session_str = str(session)
        self.assertTrue(session_str.startswith("abc:"))


class TranscriptModelTests(TestCase):
    def test_can_save_and_load(self):
        session = Session.objects.create(session_id="abc")
        transcript = Transcript(session=session)
        transcript.save()
        self.assertEqual(Transcript.objects.count(), 1)
        self.assertEqual(Transcript.objects.first(), transcript)

    def test_string(self):
        session = Session.objects.create(session_id="abc")
        transcript = Transcript.objects.create(session=session)
        transcript_str = str(transcript)
        self.assertTrue(transcript_str.startswith("abc:"))


class ReplyModelTests(TestCase):
    def test_can_save_and_load(self):
        session = Session.objects.create(session_id="abc")
        reply = Reply(session=session)
        reply.save()
        self.assertEqual(Reply.objects.count(), 1)
        self.assertEqual(Reply.objects.first(), reply)

    def test_string(self):
        session = Session.objects.create(session_id="abc")
        reply = Reply.objects.create(session=session)
        reply_str = str(reply)
        self.assertTrue(reply_str.startswith("abc:"))
