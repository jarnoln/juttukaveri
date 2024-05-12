import datetime
import json
import logging
import os
import secrets
import zoneinfo

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import openai

from util.aws_api import AwsApi

from .models import Session, Transcript, Reply
from .serializers import SessionSerializer

logger = logging.getLogger(__name__)


class SessionList(APIView):
    def get(self, request):
        sessions = Session.objects.all()
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def about(request):
    logger.info("about")
    readme_path = os.path.join(settings.BASE_DIR, "README.md")
    with open(readme_path, "r") as readme_file:
        readme_content = readme_file.read()
    return Response({"readme": readme_content})


@api_view(["POST"])
def start_session(request):
    logger.info("start_session POST=%s" % request.POST.dict())
    ip = request.POST.get("ip")
    previous_sessions = Session.objects.filter(ip=ip)
    logger.info(
        "Previous sessions from ip {}: {}".format(ip, previous_sessions.count())
    )
    today = datetime.date.today()
    sessions_today = Session.objects.filter(ip=ip, created__day=today.day)
    logger.info("Previous sessions today: {}".format(sessions_today.count()))

    replies_today = Reply.objects.filter(
        session__ip=ip, session__created__day=today.day
    )
    replies_today = replies_today.count()
    logger.info("Replies today: {}".format(replies_today))
    if replies_today < 10:
        session_id = secrets.token_urlsafe(32)
        logger.info("session_id=%s" % str(session_id))
        session = Session.objects.create(session_id=session_id)
        session.ip = ip
        session.agent = request.META.get("HTTP_USER_AGENT")
        session.referer = request.META.get("HTTP_REFERER")
        session.save()
        message = "New session created"
        status_code = status.HTTP_201_CREATED
        logger.info(
            "ip={} agent={} ip={} referer={}".format(
                session.ip, session.agent, session.ip, session.referer
            )
        )
    else:
        session_id = ""
        message = "Daily message count exceeded"
        status_code = status.HTTP_429_TOO_MANY_REQUESTS
    return Response(
        {
            "id": session_id,
            "repliesToday": replies_today,
            "message": message,
        },
        status=status_code,
    )


@api_view(["POST"])
def submit_audio(request):
    """Submit resume"""
    logger.info("submit_audio")
    logger.info("request.POST=%s" % request.POST.dict())
    audio_file = request.FILES["audio"]
    session_id = request.POST["session"]
    if session_id == "":
        message = "No session ID provided"
        logger.warning(message)
        return Response(data={"message": message}, status=status.HTTP_400_BAD_REQUEST)

    messages_string = request.POST["messages"]
    echo_str = request.POST["echo"]
    language_code = request.POST["language"]

    session = Session.objects.get(session_id=session_id)
    session_reply_count = Reply.objects.filter(session=session).count()
    if session_reply_count > 10:
        message = "Reply count exceeded"
        logger.warning(message)
        return Response(
            data={"message": message}, status=status.HTTP_429_TOO_MANY_REQUESTS
        )

    if echo_str:
        echo = True
    else:
        echo = False
    messages = json.loads(messages_string)
    logger.info("messages: {}".format(str(messages)))
    openai.api_key = settings.OPENAI_API_KEY
    try:
        transcript = handle_uploaded_audio_file(
            session, audio_file, messages, echo, language_code
        )
    except openai.error.RateLimitError as exc:
        logger.warning("No more OpenAI credits or rate limits exceeded: {}".format(exc))
        message = "OpenAI rate limits exceeded"
        return Response(
            data={"message": message}, status=status.HTTP_429_TOO_MANY_REQUESTS
        )
    return Response(transcript)


def handle_uploaded_audio_file(
    session,
    audio_file,
    messages: list,
    echo: bool = False,
    language_code: str = "fi-FI",
) -> dict:
    """Save incoming audio to file, send it to OpenAI Whisper to transcribe to text"""
    logger.info("handle_uploaded_audio_file")
    # Save to file
    with open("audio.wav", "wb+") as local_audio_file:
        for chunk in audio_file.chunks():
            local_audio_file.write(chunk)

    # Upload file to OpenAI Whisper ro transcribe it to text
    opened_audio_file = open("audio.wav", "rb")
    openai.api_key = settings.OPENAI_API_KEY
    # Whisper uses two-letter ISO-639-1 language codes while AWS Polly uses longer language codes with hyphen
    language = language_code.split("-")[0]
    if language == "cmn":
        language = "zh"
    transcript = openai.Audio.transcribe(
        "whisper-1", file=opened_audio_file, language=language
    )
    logger.info("Transcript:")
    logger.info(transcript)
    transcript_text = transcript["text"]
    Transcript.objects.create(session=session, text=transcript_text)

    if echo:
        # Just repeat what user said without calling Chat
        response_text = transcript_text
    else:
        # Add transcribed text to context messages and send it to OpenAI ChatCompletion
        messages.append({"role": "user", "content": transcript_text})
        response_text = create_response_text(messages)

    aws_api = AwsApi()
    # local_file_path = aws_api.text_to_speech(transcript_text)
    # Convert received response to voice audio using Amazon Polly

    timestamp = datetime.datetime.now(
        tz=zoneinfo.ZoneInfo(settings.TIME_ZONE)
    ).strftime("%Y-%m-%d_%H-%M-%S")
    file_name = "{}_{}_response.mp3".format(timestamp, session.session_id)
    local_file_path = aws_api.text_to_speech(response_text, file_name, language_code)

    # Save generated audio file to S3 and send URL to frontend
    audio_url = aws_api.upload_file_to_s3(local_file_path)
    Reply.objects.create(session=session, audio_url=audio_url, text=response_text)
    return {
        "transcript": transcript_text,
        "responseText": response_text,
        "audioUrl": audio_url,
    }


def create_response_text(messages: list) -> str:
    logger.info("Sending messages to OpenAI ChatCompletion API:")
    logger.info(messages)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    logger.info("Response from ChatCompletion:")
    logger.info(response)
    response_text = str(response.choices[0]["message"]["content"])
    return response_text
