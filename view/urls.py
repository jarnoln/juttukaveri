from django.urls import path

from . import views

urlpatterns = [
    path("j/", views.juttukaveri, name="juttukaveri"),
    path("", views.index, name="index"),
]
