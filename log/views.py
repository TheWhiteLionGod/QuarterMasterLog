from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.db.models import Model, Prefetch
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import logout
from typing import Callable, Any, Type, Concatenate
from uuid import UUID
from .models import *
from .forms import *

type ViewFunctions[**P] = Callable[Concatenate[HttpRequest, P], HttpResponse]
def logged_in[**P](func: ViewFunctions[P]) -> ViewFunctions[P]:
    def wrapper(response: HttpRequest, *args: P.args, **kwargs: P.kwargs) -> HttpResponse:
        if response.user.is_authenticated:
            return func(response, *args, **kwargs)
        return redirect('/')
    return wrapper

def index(response: HttpRequest) -> HttpResponse:
    equipment = Equipment.objects.select_related(
        "equipmentbin", "foodbin", "cooler", "waterjug"
    )

    equipmentbins = [e for e in equipment if hasattr(e, "equipmentbin")]
    foodbins = [e for e in equipment if hasattr(e, "foodbin")]
    coolers = [e for e in equipment if hasattr(e, "cooler")]
    waterjugs = [e for e in equipment if hasattr(e, "waterjug")]

    return render(response, "index.html", {
        "campsites": CampSite.objects.all().order_by("-id"),
        "equipmentbins": equipmentbins,
        "foodbins": foodbins,
        "coolers": coolers,
        "waterjugs": waterjugs,
    })

def camp(response: HttpRequest, pubkey: UUID) -> HttpResponse:
    assignments_qs = Assignment.objects.select_related(
        "equipment",
        "equipment__equipmentbin",
        "equipment__foodbin",
        "equipment__cooler",
        "equipment__waterjug",
    )

    camp = get_object_or_404(
        CampSite.objects.prefetch_related(
            Prefetch("assignments", queryset=assignments_qs)
        ),
        pubkey=pubkey,
    )

    return render(response, "camp.html", {"camp": camp})

def equipment(response: HttpRequest, pubkey: UUID) -> HttpResponse:
    try:
        equipment = Equipment.objects.get(pubkey=pubkey)
    except Equipment.DoesNotExist:
        return redirect('/')

    return render(response, 'equipment.html', {'equipment': equipment})

form_types: dict[str, Type[ModelForm[Any]]] = {
    "campsite": CampSiteForm,
    "equipmentbin": EquipmentBinForm,
    "foodbin": FoodBinForm,
    "cooler": CoolerForm,
    "waterjug": WaterJugForm,
    "assignment": AssignmentForm
}

cls_types: dict[str, Type[Model]] = {
    "campsite": CampSite,
    "equipmentbin": EquipmentBin,
    "foodbin": FoodBin,
    "cooler": Cooler,
    "waterjug": WaterJug,
    "assignment": Assignment
}

@logged_in
def form(response: HttpRequest, type: str) -> HttpResponse:
    form_cls = form_types.get(type)
    if form_cls is None:
        return redirect('/')

    form = form_cls(response.POST) if response.method == "POST" else form_cls()
    if form.is_valid():
        form.save()
        return redirect('/')
    
    return render(response, "form.html", {"form": form, "edit": False})

@logged_in
def edit(response: HttpRequest, type: str, pubkey: UUID) -> HttpResponse:
    model_cls = cls_types.get(type)
    if model_cls is None:
        return redirect('/')

    form_cls = form_types.get(type)
    if form_cls is None:
        return redirect('/')
    
    try:
        model = model_cls.objects.get(pubkey=pubkey)
    except model_cls.DoesNotExist:
        return redirect('/')
    
    if response.method == "POST":
        if "delete" in response.POST:
            model.delete()
            return redirect('/')

        form = form_cls(response.POST, instance=model)
        if form.is_valid():
            form.save()
            return redirect('/')
    else: 
        form = form_cls(instance=model)

    return render(response, "form.html", {"form": form, "edit": True})

@logged_in
def custom_logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('/')
