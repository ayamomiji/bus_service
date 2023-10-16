import json

from django import forms
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from bus_notifiers.tdx import client as tdx

from .models import Notifier


def collection(request):
    if request.method == "GET":
        return index(request)
    if request.method == "POST":
        return create(request)


def index(request):
    paginator = Paginator(Notifier.objects.order_by("-id"), 20)
    page_number = request.GET.get("page", None)
    if page_number is None or "":
        page_number = 1
    page = paginator.page(page_number)
    notifiers = page.object_list
    notifiers_as_dict = [n.as_json() for n in notifiers]
    return JsonResponse({"notifiers": notifiers_as_dict})


class CreateForm(forms.Form):
    route = forms.CharField(required=True)
    stop = forms.CharField(required=True)
    direction = forms.ChoiceField(
        required=True, choices=[(0, "Departure"), (1, "Return")]
    )
    email = forms.CharField(required=True)

    def validate_route(self, route):
        data = tdx.get_route(route, 1, 0)
        if len(data) == 0:
            raise forms.ValidationError("invalid route")

    def validate_stop(self, route, stop):
        skip = 0
        while True:
            data = tdx.get_stop_of_route(route, 30, skip)
            if len(data) == 0:
                raise forms.ValidationError("invalid stop")
            for row in data:
                for stop_row in row["Stops"]:
                    if stop_row["StopName"]["Zh_tw"] == stop:
                        return
            skip += 30

    def clean(self):
        cleaned_data = super().clean()
        self.validate_route(cleaned_data["route"])
        self.validate_stop(cleaned_data["route"], cleaned_data["stop"])

        return cleaned_data


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
