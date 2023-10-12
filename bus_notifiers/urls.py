from django.urls import path

from . import views

app_name = "bus_notifiers"

urlpatterns = [
    path("", views.index, name="index"),
]
