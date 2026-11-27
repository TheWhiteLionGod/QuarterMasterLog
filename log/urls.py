from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("form/<str:type>", views.form, name="form"),
    path("edit/<str:type>/<uuid:pubkey>", views.edit, name="edit"),
    path("camp/<uuid:pubkey>", views.camp, name="camp"),
    path("equipment/<uuid:pubkey>", views.equipment, name="equipment"),
    path("logout/", views.custom_logout, name="logout")
]
