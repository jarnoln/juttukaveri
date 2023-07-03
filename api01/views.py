from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import openai

from util.aws_api import AwsApi


@api_view(['POST'])
def submit_audio(request):
    """ Submit resume """
    print('request.FILES=%s' % request.FILES)
    audio_file = request.FILES['audio']
    openai.api_key = settings.OPENAI_API_KEY
    # transcript = openai.Audio.transcribe('whisper-1', file=audio_file, language='fi')
    transcript = handle_uploaded_audio_file(audio_file)
    return Response(transcript)


def handle_uploaded_audio_file(audio_file):
    with open('audio.wav', 'wb+') as local_audio_file:
        for chunk in audio_file.chunks():
            local_audio_file.write(chunk)

    opened_audio_file = open('audio.wav', 'rb')
    openai.api_key = settings.OPENAI_API_KEY
    transcript = openai.Audio.transcribe('whisper-1', file=opened_audio_file, language='fi')
    print('Transcript:')
    print(transcript)
    transcript_text = transcript['text']
    aws_api = AwsApi()
    local_file_path = aws_api.text_to_speech(transcript_text)
    audio_url = aws_api.upload_file_to_s3(local_file_path)
    return {
        'transcript': transcript_text,
        'audioUrl': audio_url
    }
