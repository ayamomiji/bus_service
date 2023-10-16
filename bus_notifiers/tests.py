import json

from django.test import TestCase
from django.urls import reverse

from .models import Notifier


class TestModels(TestCase):
    def test_notifier_can_create(self):
        Notifier.objects.create(route="307", stop="捷運南京復興站")


class TestViews(TestCase):
    def test_index(self):
        response = self.client.get(reverse("bus_notifiers:collection"))
        self.assertEqual(
            response.content.decode("utf-8"), json.dumps({"notifiers": []})
        )

    def test_index_with_data(self):
        notifier = Notifier.objects.create(route="307", stop="捷運南京復興站")
        response = self.client.get(reverse("bus_notifiers:collection"))
        self.assertEqual(
            response.content.decode("utf-8"),
            json.dumps({"notifiers": [notifier.as_json()]}),
        )

    def test_create_success(self):
        response = self.client.post(
            reverse("bus_notifiers:collection"),
            json.dumps({"route": "307", "stop": "捷運南京復興站"}),
            content_type="application/json",
        )
        self.assertEqual(
            response.content.decode("utf-8"),
            json.dumps({"notifier": Notifier.objects.last().as_json()}),
        )

    def test_create_with_invalid_data(self):
        response = self.client.post(
            reverse("bus_notifiers:collection"),
            json.dumps({"route": "沒有這台車", "stop": "沒有這個站"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 422)

    def test_destroy_success(self):
        notifier = Notifier.objects.create(route="307", stop="捷運南京復興站")
        response = self.client.delete(
            reverse("bus_notifiers:member", kwargs={"id": notifier.id})
        )
        self.assertEqual(
            response.content.decode("utf-8"),
            json.dumps({"ok": True}),
        )

    def test_destroy_with_not_found(self):
        response = self.client.delete(reverse("bus_notifiers:member", kwargs={"id": 1}))
        self.assertEqual(
            response.content.decode("utf-8"),
            json.dumps({"error": "Not found"}),
        )
