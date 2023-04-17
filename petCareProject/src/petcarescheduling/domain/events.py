from abc import ABC
from dataclasses import dataclass

from .models import PetService


class Event(ABC):
    pass

@dataclass
class PetServiceAdded(Event):
    service_id: int
    service_name: str
    price: str
    pet_species: str
