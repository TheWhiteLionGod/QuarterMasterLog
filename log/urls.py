from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("form/<str:type>", views.form, name="form")
]
