from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from bus_data.models import Route


def index(request):
    return HttpResponse("Hello, world.")


def routes(request):
    q = request.GET.get("q", None)
    routes = Route.objects.filter(name__icontains=q).all()[0:10]

    return JsonResponse({"routes": [route.as_json() for route in routes]})
