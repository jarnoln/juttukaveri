from django.urls import path
from .views import submit_audio


urlpatterns = [
    path('submit_audio', submit_audio, name='submit_audio')
]
