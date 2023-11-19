from django.urls import path

from . import views

urlpatterns = [
    path("info", views.index, name="index"),
    path("schedule", views.schedule, name="schedule"),

]
