from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class CampSite(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)]
    )

    def __str__(self) -> str:
        return f"{self.name} {self.year}"

class Equipment(models.Model):
    label = models.CharField(max_length=100)

    @property
    def real_instance(self):
        if hasattr(self, '_real_instance_cache'):
            return self._real_instance_cache

        self._real_instance_cache = self
        for subclass in self.__class__.__subclasses__():
            attr_name = subclass.__name__.lower()
            try:
                self._real_instance_cache = getattr(self, attr_name)
                break
            except ObjectDoesNotExist:
                continue

        return self._real_instance_cache
        
    def __str__(self) -> str:
        if type(self) is Equipment:
            return str(self.real_instance)
        return f"Equipment {self.label}"

class EquipmentBin(Equipment):
    has_stove = models.BooleanField()
    has_cutting_board = models.BooleanField()
    has_kitchen_knife = models.BooleanField()
    mittens = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9)])
    has_solid_spatula = models.BooleanField()
    has_slotted_spatula = models.BooleanField()
    has_tongs = models.BooleanField()
    has_solid_spoon = models.BooleanField()
    has_slotted_spoon = models.BooleanField()
    has_cooking_fork = models.BooleanField()
    has_can_opener = models.BooleanField()
    has_peeler = models.BooleanField()
    has_wisk = models.BooleanField()
    has_measuring_cup = models.BooleanField()
    has_griddle = models.BooleanField()
    has_strainer = models.BooleanField()
    washing_bins = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9)])

    def __str__(self) -> str:
        return f"Equipment Bin {self.label}"

class FoodBin(Equipment):
    def __str__(self) -> str:
        return f"Food Bin {self.label}"

class Cooler(Equipment):
    def __str__(self) -> str:
        return f"Cooler {self.label}"

class WaterJug(Equipment):
    def __str__(self) -> str:
        return f"Water Jug {self.label}"

class Assignment(models.Model):
    campsite = models.ForeignKey(CampSite, on_delete=models.CASCADE, related_name='assignments')
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, related_name='assignments')
    person = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.person} took {self.equipment} on {self.campsite}"
