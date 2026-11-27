from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Model, Field, CharField, PositiveSmallIntegerField, BooleanField, UUIDField, ForeignKey, CASCADE, PROTECT
import uuid

class CampSite(Model):
    pubkey: Field[uuid.UUID, uuid.UUID] = UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    name: Field[str, str] = CharField(max_length=100)
    year: Field[int, int] = PositiveSmallIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)]
    )

    def __str__(self) -> str:
        return f"{self.name} {self.year}"

class Equipment(Model):
    pubkey: Field[uuid.UUID, uuid.UUID] = UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    label: Field[str, str] = CharField(max_length=100)

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

    @property
    def model_name(self):
        return self.real_instance._meta.model_name

    @property
    def fields(self):
        return [(f.verbose_name, getattr(self.real_instance, f.name)) for f in self.real_instance._meta.fields]
        
    def __str__(self) -> str:
        if type(self) is Equipment:
            return str(self.real_instance)
        return f"Equipment {self.label}"

class EquipmentBin(Equipment):
    has_stove: Field[bool, bool] = BooleanField()
    has_cutting_board: Field[bool, bool] = BooleanField()
    has_kitchen_knife: Field[bool, bool] = BooleanField()
    mittens: Field[int, int] = PositiveSmallIntegerField(validators=[MaxValueValidator(9)])
    has_solid_spatula: Field[bool, bool] = BooleanField()
    has_slotted_spatula: Field[bool, bool] = BooleanField()
    has_tongs: Field[bool, bool] = BooleanField()
    has_solid_spoon: Field[bool, bool] = BooleanField()
    has_slotted_spoon: Field[bool, bool] = BooleanField()
    has_cooking_fork: Field[bool, bool] = BooleanField()
    has_can_opener: Field[bool, bool] = BooleanField()
    has_peeler: Field[bool, bool] = BooleanField()
    has_wisk: Field[bool, bool] = BooleanField()
    has_measuring_cup: Field[bool, bool] = BooleanField()
    has_griddle: Field[bool, bool] = BooleanField()
    has_strainer: Field[bool, bool] = BooleanField()
    washing_bins: Field[int, int] = PositiveSmallIntegerField(validators=[MaxValueValidator(9)])

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

class Assignment(Model):
    pubkey: Field[uuid.UUID, uuid.UUID] = UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    campsite: Field[CampSite, CampSite] = ForeignKey(CampSite, on_delete=CASCADE, related_name='assignments')
    equipment: Field[Equipment, Equipment] = ForeignKey(Equipment, on_delete=PROTECT, related_name='assignments')
    person: Field[str, str] = CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.person} Took {self.equipment} On {self.campsite}"
