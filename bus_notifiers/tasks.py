from bus_notifiers.models import Notifier
from bus_service.celery import app


@app.task(bind=True, ignore_result=True)
def check_notifiers(self):
    notifiers = Notifier.objects.all()
    for notifier in notifiers:
        check_notifier.delay(notifier.id, 30, 0)


@app.task(bind=True, ignore_result=True)
def check_notifier(self, notifier_id, top, skip):
    notifier = Notifier.objects.get(pk=notifier_id)
    route = notifier.route
    stop = notifier.stop

    # data = get_route_near_stop(route.name, top, skip)

    # for row in data:
    #     print(row["StopUID"])
    #     stop = route.stop_set.get(tdx_id=row["StopUID"])
    #     print(stop.name)
