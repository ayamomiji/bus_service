from bus_service.celery import app


@app.task(bind=True, ignore_result=True)
def download_data(self):
    print(f"Request: {self.request!r}")
