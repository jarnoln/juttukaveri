from django.urls import path
from .views import about, start_session, submit_audio, SessionList


urlpatterns = [
    path("about", about, name="about"),
    path("sessions", SessionList.as_view(), name="session_list"),
    path("start_session", start_session, name="start_session"),
    path("submit_audio", submit_audio, name="submit_audio"),
]
