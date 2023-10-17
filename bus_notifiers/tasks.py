from bus_notifiers.models import Notifier
from bus_notifiers.tdx.client import get_estimated_time_of_arrive_with_stop
from bus_service.celery import app


@app.task(bind=True, ignore_result=True)
def check_notifiers(self):
    notifiers = Notifier.stale_objects.all()
    for notifier in notifiers:
        check_notifier.delay(notifier.id, 30, 0)


@app.task(bind=True, ignore_result=True)
def check_notifier(self, notifier_id, top, skip):
    notifier = Notifier.objects.get(pk=notifier_id)
    route = notifier.route
    stop = notifier.stop
    direction = notifier.direction

    data = get_estimated_time_of_arrive_with_stop(
        route, stop, direction, top=top, skip=skip
    )
    notifier.notify([row["EstimateTime"] for row in data if row["EstimateTime"] < 1000])

    if len(data) > top:
        check_notifier.delay(notifier.id, top, skip + top)
