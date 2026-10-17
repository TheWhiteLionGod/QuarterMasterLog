from django.contrib import admin
from .models import CampSite, Equipment, EquipmentBin, FoodBin, Cooler, WaterJug, Assignment

admin.site.register(CampSite)
admin.site.register(Equipment)
admin.site.register(EquipmentBin)
admin.site.register(FoodBin)
admin.site.register(Cooler)
admin.site.register(WaterJug)
admin.site.register(Assignment)
