from datetime import timedelta

from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
from django.utils import timezone


class StaleNotifierManager(models.Manager):
    def get_queryset(self):
        # 三分鐘內不重複通知
        three_minutes_ago = timezone.now() - timedelta(minutes=3)
        return (
            super()
            .get_queryset()
            .filter(
                Q(last_notified_at__isnull=True)
                | Q(last_notified_at__lte=three_minutes_ago)
            )
        )


class Notifier(models.Model):
    Direction = models.IntegerChoices("Direction", "DEPARTURE RETURN")

    route = models.CharField(max_length=255)
    stop = models.CharField(max_length=255)
    direction = models.IntegerField(choices=Direction.choices)
    email = models.CharField(max_length=255)
    last_notified_at = models.DateTimeField(null=True, default=None)

    objects = models.Manager()
    stale_objects = StaleNotifierManager()

    def as_json(self):
        return {"id": self.id, "route": self.route, "stop": self.stop}

    def notify(self, times):
        self.notify_by_email(min(times))
        self.last_notified_at = timezone.now()
        self.save()

    def notify_by_email(self, time):
        subject = "公車到站通知"
        message = f"公車{self.route} ({self.get_direction_display()}) 將在 {time} 秒後抵達 {self.stop}!"
        if self.email is None or self.email == "":
            print("WARN: email 未提供")
            return
        from_email = "no-reply@example.com"
        recipient_list = [self.email]
        try:
            send_mail(subject, message, from_email, recipient_list)
        except ConnectionRefusedError:
            print("WARN: Connection refused. 無法連上 SMTP Server.")
            print(message)
