from django.shortcuts import render, redirect
from django.forms import ModelForm
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

def form(response, type: str):
    form_cls = form_types.get(type)
    if form_cls is None:
        return redirect('/')

    form = form_cls(response.POST) if response.method == "POST" else form_cls()
    if form.is_valid():
        form.save()
        return redirect('/')
    
    return render(response, "form.html", {"form": form})

def camp(response, id: int):
    camp = CampSite.objects.get(id=id)
    return render(response, "camp.html", {"camp": camp})
