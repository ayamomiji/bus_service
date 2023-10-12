from django.db import models


class Notifier(models.Model):
    route = models.ForeignKey("bus_data.Route", on_delete=models.CASCADE, null=False)
    stop = models.ForeignKey("bus_data.Stop", on_delete=models.CASCADE, null=False)
    email = models.CharField(max_length=255)

    def as_json(self):
        return {"id": self.id, "route": self.route.name, "stop": self.stop.name}
