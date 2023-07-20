from django.urls import path
from .views import start_session, submit_audio


urlpatterns = [
    path('submit_audio', submit_audio, name='submit_audio'),
    path('start_session', start_session, name='start_session')
]
