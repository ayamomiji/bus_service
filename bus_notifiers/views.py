import json

from django import forms
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from bus_data.models import Route, Stop

from .models import Notifier


def collection(request):
    if request.method == "GET":
        return index(request)
    if request.method == "POST":
        return create(request)


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


class CreateForm(forms.Form):
    route_id = forms.IntegerField(required=True)
    stop_id = forms.IntegerField(required=True)

    def clean_route_id(self):
        id = self.cleaned_data["route_id"]
        if not Route.objects.filter(pk=id).exists():
            raise forms.ValidationError("route_id is not valid")
        return id

    def clean_stop_id(self):
        id = self.cleaned_data["stop_id"]
        if not Stop.objects.filter(pk=id).exists():
            raise forms.ValidationError("stop_id is not valid")
        return id


def create(request):
    params = json.loads(request.body)
    form = CreateForm(params)
    if form.is_valid():
        # create notifier
        notifier = Notifier(**form.cleaned_data)
        notifier.save()
        return JsonResponse({"notifier": notifier.as_json()})
    else:
        return JsonResponse(
            {"error": "Invalid parameters", "errors": dict(form.errors)}, status=422
        )


def member(request, id):
    if request.method == "DELETE":
        return destroy(request, id)
    return JsonResponse({"error": "Method not allowed"}, status=405)


def destroy(request, id):
    try:
        notifier = Notifier.objects.get(pk=id)
        notifier.delete()
        return JsonResponse({"ok": True})
    except Notifier.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
