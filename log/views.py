from django.shortcuts import render
from .models import CampSite
from .forms import AssignmentForm

# Create your views here.
def index(response):
    return render(response, "index.html", {"campsites": CampSite.objects.all()})

def form(response):
    f = AssignmentForm() 
    return render(response, "form.html", {"form": f})
