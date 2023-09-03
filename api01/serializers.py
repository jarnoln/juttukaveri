from rest_framework import serializers
from .models import Session, Transcript, Reply


class TranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = ['session', 'audio_url', 'text', 'created']


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['session', 'audio_url', 'text', 'created']


class SessionSerializer(serializers.ModelSerializer):
    transcripts = TranscriptSerializer(many=True, read_only=True)
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = ['session_id', 'ip', 'agent', 'referer', 'created', 'transcripts', 'replies']
