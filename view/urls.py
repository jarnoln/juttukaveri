from django.urls import path

from . import views

urlpatterns = [
    path("sessiot/", views.sessions, name="sessions"),
    path("j/", views.juttukaveri, name="juttukaveri"),
    path("", views.index, name="index"),
]
