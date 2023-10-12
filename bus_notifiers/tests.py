import json
from django.test import TestCase
from django.urls import reverse
from bus_data.models import Route, Stop
from .models import Notifier


class TestModels(TestCase):
    def create_route(self):
        route = Route()
        route.save()
        return route

    def create_stop(self):
        stop = Stop()
        stop.save()
        return stop

    def test_notifier_can_create(self):
        route = self.create_route()
        stop = self.create_stop()
        notifier = Notifier(route=route, stop=stop)
        notifier.save()


class TestViews(TestCase):
    def test_index(self):
        response = self.client.get(reverse("bus_notifiers:index"))
        self.assertEqual(
            response.content.decode("utf-8"), json.dumps({"notifiers": []})
        )
