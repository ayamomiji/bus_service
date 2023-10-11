from django.contrib import admin
from .models import Route, RouteStop, Stop


admin.site.register(Route)
admin.site.register(Stop)
admin.site.register(RouteStop)
