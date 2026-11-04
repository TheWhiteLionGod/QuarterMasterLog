from django.shortcuts import render, redirect
from django.forms import ModelForm
from django.db.models import Model
from typing import Type
from .models import *
from .forms import *

def index(response):
    return render(response, "index.html", {"campsites": CampSite.objects.all().order_by('-id')})

form_types: dict[str, Type[ModelForm]] = {
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

def form(response, type: str):
    form_cls = form_types.get(type)
    if form_cls is None:
        return redirect('/')

    form = form_cls(response.POST) if response.method == "POST" else form_cls()
    if form.is_valid():
        form.save()
        return redirect('/')
    
    return render(response, "form.html", {"form": form})

def edit(response, type: str, id: int):
    model_cls = cls_types.get(type)
    if model_cls is None:
        return redirect('/')

    try:
        model = model_cls.objects.get(id=id)
    except model_cls.DoesNotExist:
        return redirect('/')

    form_cls = form_types.get(type)
    form = form_cls(response.POST, instance=model) if response.method == "POST" else form_cls(instance=model)

    if response.method == "POST" and form.is_valid():
        form.save()
        return redirect('/')
    
    return render(response, "form.html", {"form": form})

def camp(response, id: int):
    camp = CampSite.objects.get(id=id)
    return render(response, "camp.html", {"camp": camp})
