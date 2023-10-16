from django.db import models


class Route(models.Model):
    tdx_id = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50)
    # Departure = 去程, Return = 回程, Loop = 迴圈
    direction = models.CharField(max_length=50)
    # 這也會一併定義 Stop#route_set
    stop_set = models.ManyToManyField("Stop", through="RouteStop")

    def as_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "direction": self.direction,
            "stops": [stop.as_json() for stop in self.stop_set.all()],
        }

    class Meta:
        indexes = [models.Index(fields=["tdx_id", "direction"])]


class Stop(models.Model):
    tdx_id = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50)

    def as_json(self):
        return {"id": self.id, "name": self.name}

    class Meta:
        indexes = [models.Index(fields=["tdx_id"])]


# 增加 default_scope, 按照 order 排序
class RouteStopManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("order")


class RouteStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    order = models.IntegerField(db_index=True)

    objects = RouteStopManager()
