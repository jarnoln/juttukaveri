from django.urls import path
from .views import submit_audio, submit_audio_file


urlpatterns = [
    path('submit_audio_file', submit_audio_file, name='submit_audio_file'),
    path('submit_audio', submit_audio, name='submit_audio')
]
