from django.test import TestCase
from bus_data.models import Route, Stop


class TestModel(TestCase):
    def setUp(self):
        Route.objects.create(name="100")
        Stop.objects.create(name="Stop A")

    def test_model_relations_work(self):
        route = Route.objects.get(name="100")
        stop = Stop.objects.get(name="Stop A")
        route.stop_set.add(stop, through_defaults={"order": 1})
        self.assertEqual(route.stop_set.count(), 1)
        self.assertEqual(stop.route_set.count(), 1)
