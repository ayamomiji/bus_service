from django.db import models


class Route(models.Model):
    name = models.CharField(max_length=50)
    # Departure = 去程, Return = 回程
    direction = models.CharField(max_length=50)
    # 這也會一併定義 Stop#route_set
    stop_set = models.ManyToManyField("Stop", through="RouteStop")


class Stop(models.Model):
    name = models.CharField(max_length=50)


# 增加 default_scope, 按照 order 排序
class RouteStopManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("order")


class RouteStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    order = models.IntegerField(db_index=True)

    objects = RouteStopManager()
