from django.db import models


class Notifier(models.Model):
    route = models.CharField(max_length=255)
    stop = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def as_json(self):
        return {"id": self.id, "route": self.route, "stop": self.stop}
