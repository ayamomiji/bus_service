from django.db import models


class Notifier(models.Model):
    Direction = models.IntegerChoices("Direction", "DEPARTURE RETURN")

    route = models.CharField(max_length=255)
    stop = models.CharField(max_length=255)
    direction = models.CharField(max_length=50, choices=Direction.choices)
    email = models.CharField(max_length=255)

    def as_json(self):
        return {"id": self.id, "route": self.route, "stop": self.stop}
