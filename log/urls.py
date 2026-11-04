from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("form/<str:type>", views.form, name="form"),
    path("edit/<str:type>/<int:id>", views.edit, name="edit"),
    path("camp/<int:id>", views.camp, name="camp")
]
