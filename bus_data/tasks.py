import traceback

from bus_data.models import Route, RouteStop, Stop
from bus_data.tdx.client import get_stops_of_routes
from bus_service.celery import app

direction_map = {0: "Departure", 1: "Return", 2: "Loop"}


@app.task(bind=True, ignore_result=True)
def download_data(self):
    RouteStop.objects.all().delete()
    download_partial_data.delay(30, 0)


@app.task(bind=True, ignore_result=True)
def download_partial_data(self, top, skip):
    try:
        data = get_stops_of_routes(top, skip)
        for row in data:
            _handle_row(row)
        # there are more data to fetch
        if len(data) >= top:
            download_partial_data.delay(top, skip + top)
    except Exception as exc:
        traceback.print_exc()
        self.retry(exc=exc)


def _handle_row(row):
    route = _upsert_route(row)

    for stop_row in row["Stops"]:
        stop = _upsert_stop(stop_row)
        order = stop_row["StopSequence"]
        try:
            rs = RouteStop.objects.get(route=route, stop=stop)
            rs.order = order
            rs.save()
        except RouteStop.DoesNotExist:
            RouteStop.objects.create(route=route, stop=stop, order=order)


def _upsert_route(row):
    tdx_id = row["RouteUID"]
    name = row["RouteName"]["Zh_tw"]
    direction = direction_map[row["Direction"]]

    (route, _created) = Route.objects.get_or_create(tdx_id=tdx_id, direction=direction)
    route.name = name
    route.save()
    return route


def _upsert_stop(row):
    tdx_id = row["StopUID"]
    name = row["StopName"]["Zh_tw"]

    (stop, _created) = Stop.objects.get_or_create(tdx_id=tdx_id)
    stop.name = name
    stop.save()
    return stop
