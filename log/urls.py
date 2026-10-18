from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("camp/<int:id>", views.campsite, name="camp")
]
