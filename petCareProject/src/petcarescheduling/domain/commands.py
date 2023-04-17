from dataclasses import dataclass
from typing import Optional

class Command:
    pass


@dataclass
class CreateService(Command):
    service_id: int
    service_name: str
    price: int
    pet_species: str


@dataclass
class UpdateService(Command):
    service_name: str
    price: int
