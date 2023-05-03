from dataclasses import dataclass
from typing import Optional

class Command:
    pass


@dataclass
class CreateService(Command):
    #service_id: int
    service_name: str
    price: int
    pet_species: str
    qty: int


@dataclass
class AllocateService(Command):
    customer_id: int
    service_name: str
    pet_species: str

@dataclass
class ChangeBatchQuantity(Command):
    service_name: str
    qty: int
