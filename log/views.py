from django.shortcuts import render
from .models import CampSite
from .forms import EquipmentBinForm

# Create your views here.
def index(response):
    return render(response, "index.html", {"campsites": CampSite.objects.all()})

def form(response):
    if response.method == "POST":
        print(response.POST)
    f = EquipmentBinForm() 
    return render(response, "form.html", {"form": f})
