from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from .models import Notifier


def index(request):
    paginator = Paginator(
        Notifier.objects.prefetch_related("route", "stop").order_by("-id"), 20
    )
    page_number = request.GET.get("page", None)
    if page_number is None or "":
        page_number = 1
    page = paginator.page(page_number)
    notifiers = page.object_list
    notifiers_as_dict = [n.as_json() for n in notifiers]
    return JsonResponse({"notifiers": notifiers_as_dict})
