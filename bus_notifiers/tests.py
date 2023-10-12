import json
from django.test import TestCase
from django.urls import reverse
from bus_data.models import Route, Stop
from .models import Notifier


class TestHelpers:
    def create_route(self):
        route = Route()
        route.save()
        return route

    def create_stop(self):
        stop = Stop()
        stop.save()
        return stop

    def create_notifier(self, route=None, stop=None):
        if route is None:
            route = self.create_route()
        if stop is None:
            stop = self.create_stop()
        notifier = Notifier(route=route, stop=stop)
        notifier.save()
        return notifier


class TestModels(TestCase, TestHelpers):
    def test_notifier_can_create(self):
        route = self.create_route()
        stop = self.create_stop()
        notifier = Notifier(route=route, stop=stop)
        notifier.save()


class TestViews(TestCase, TestHelpers):
    def test_index(self):
        response = self.client.get(reverse("bus_notifiers:collection"))
        self.assertEqual(
            response.content.decode("utf-8"), json.dumps({"notifiers": []})
        )

    def test_create_success(self):
        route = self.create_route()
        stop = self.create_stop()
        response = self.client.post(
            reverse("bus_notifiers:collection"),
            json.dumps({"route_id": route.id, "stop_id": stop.id}),
            content_type="application/json",
        )
        self.assertEqual(
            response.content.decode("utf-8"),
            json.dumps({"notifier": Notifier.objects.last().as_json()}),
        )

    def test_create_fail(self):
        response = self.client.post(
            reverse("bus_notifiers:collection"),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 422)

    def test_destroy_success(self):
        notifier = self.create_notifier()
        response = self.client.delete(
            reverse("bus_notifiers:member", kwargs={"id": notifier.id})
        )
        self.assertEqual(
            response.content.decode("utf-8"),
            json.dumps({"ok": True}),
        )

    def test_destroy_fail(self):
        response = self.client.delete(reverse("bus_notifiers:member", kwargs={"id": 1}))
        self.assertEqual(
            response.content.decode("utf-8"),
            json.dumps({"error": "Not found"}),
        )
