from django import forms
from .models import *

class CampSiteForm(forms.ModelForm):
    class Meta:
        model = CampSite
        fields = '__all__'

class EquipmentBinForm(forms.ModelForm):
    class Meta:
        model = EquipmentBin
        fields = '__all__'

class FoodBinForm(forms.ModelForm):
    class Meta:
        model = FoodBin
        fields = '__all__'

class CoolerForm(forms.ModelForm):
    class Meta:
        model = Cooler
        fields = '__all__'

class WaterJugForm(forms.ModelForm):
    class Meta:
        model = WaterJug
        fields = '__all__'

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'
