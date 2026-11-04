from typing import Any
from django import forms
from .models import *

class CampSiteForm(forms.ModelForm[Any]):
    class Meta:
        model = CampSite
        fields = '__all__'

class EquipmentBinForm(forms.ModelForm[Any]):
    class Meta:
        model = EquipmentBin
        fields = '__all__'

class FoodBinForm(forms.ModelForm[Any]):
    class Meta:
        model = FoodBin
        fields = '__all__'

class CoolerForm(forms.ModelForm[Any]):
    class Meta:
        model = Cooler
        fields = '__all__'

class WaterJugForm(forms.ModelForm[Any]):
    class Meta:
        model = WaterJug
        fields = '__all__'

class AssignmentForm(forms.ModelForm[Any]):
    class Meta:
        model = Assignment
        fields = '__all__'
