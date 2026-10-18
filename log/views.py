from django.shortcuts import render
from django.http import HttpResponse
from .models import CampSite

# Create your views here.
def index(response):
    return render(response, "index.html", {"campsites": CampSite.objects.all()})

def campsite(response, id: int):
    return HttpResponse(str(id))
