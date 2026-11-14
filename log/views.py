from django.shortcuts import render, redirect
from django.forms import ModelForm
from django.db.models import Model
from django.http import HttpRequest, HttpResponse
from typing import Type
from uuid import UUID
from .models import *
from .forms import *

def index(response: HttpRequest) -> HttpResponse:
    return render(response, "index.html", {
        "campsites": CampSite.objects.all().order_by('-id'), 
        "equipmentbins": EquipmentBin.objects.all(),
        "foodbins": FoodBin.objects.all(),
        "coolers": Cooler.objects.all(),
        "waterjugs": WaterJug.objects.all()
    })

def camp(response: HttpRequest, pubkey: UUID) -> HttpResponse:
    camp = CampSite.objects.get(pubkey=pubkey)
    return render(response, "camp.html", {"camp": camp})

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

def form(response: HttpRequest, type: str) -> HttpResponse:
    form_cls = form_types.get(type)
    if form_cls is None:
        return redirect('/')

    form = form_cls(response.POST) if response.method == "POST" else form_cls()
    if form.is_valid():
        form.save()
        return redirect('/')
    
    return render(response, "form.html", {"form": form, "edit": False})

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
