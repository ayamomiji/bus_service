from django.urls import path

from . import views

app_name = "bus_notifiers"

urlpatterns = [
    path("", views.collection, name="collection"),
    path("<int:id>", views.member, name="member"),
]
