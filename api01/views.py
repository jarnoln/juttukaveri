import json
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import openai

from util.aws_api import AwsApi


logger = logging.getLogger(__name__)


@api_view(['POST'])
def submit_audio(request):
    """ Submit resume """
    logger.info('submit_audio')
    # logger.info('request.FILES=%s' % request.FILES)
    logger.info('request.POST=%s' % request.POST)
    audio_file = request.FILES['audio']
    messages_string = request.POST['messages']
    messages = json.loads(messages_string)
    logger.info('messages: {}'.format(str(messages)))
    openai.api_key = settings.OPENAI_API_KEY
    # transcript = openai.Audio.transcribe('whisper-1', file=audio_file, language='fi')
    transcript = handle_uploaded_audio_file(audio_file, messages)
    return Response(transcript)


def handle_uploaded_audio_file(audio_file, messages: list) -> dict:
    """ Save incoming audio to file, send it to OpenAI Whisper to transcribe to text"""
    logger.info('handle_uploaded_audio_file')
    # Save to file
    with open('audio.wav', 'wb+') as local_audio_file:
        for chunk in audio_file.chunks():
            local_audio_file.write(chunk)

    # Upload file to OpenAI Whisper ro transcribe it to text
    opened_audio_file = open('audio.wav', 'rb')
    openai.api_key = settings.OPENAI_API_KEY
    transcript = openai.Audio.transcribe('whisper-1', file=opened_audio_file, language='fi')
    logger.info('Transcript:')
    logger.info(transcript)
    transcript_text = transcript['text']

    # Add transcribed text to context messages and send it to OpenAI ChatCompletion
    messages.append({'role': 'user', 'content': transcript_text})
    response_text = create_response_text(messages)

    aws_api = AwsApi()
    # local_file_path = aws_api.text_to_speech(transcript_text)
    # Convert received response to voice audio using Amazon Polly
    local_file_path = aws_api.text_to_speech(response_text)

    # Save generated audio file to S3 and send URL to frontend
    audio_url = aws_api.upload_file_to_s3(local_file_path)
    return {
        'transcript': transcript_text,
        'responseText': response_text,
        'audioUrl': audio_url,
    }


def create_response_text(messages: list) -> str:
    logger.info('Sending messages to OpenAI ChatCompletion API:')
    logger.info(messages)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    logger.info('Response from ChatCompletion:')
    logger.info(response)
    response_text = response.choices[0]['message']['content']
    return response_text
