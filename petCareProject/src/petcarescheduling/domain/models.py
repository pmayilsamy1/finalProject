from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Set
from . import commands, events

class Service:
    def __init__(self, service_name: str, petservices: List[PetService], version_number: int = 0):
        self.service_name = service_name
        self.petservices = petservices
        self.version_number = version_number
        self.events = []  # type: List[events.Event]

    def allocate(self, customer: Customer) -> str:
        try:
            petservice1 = next(b for b in sorted(self.petservices) if b.can_allocate(customer))
            petservice1.allocate(customer)
            self.version_number += 1
            self.events.append(
                events.Allocated(
                    customer_id=customer.customer_id,
                    service_name=customer.service_name,
                    pet_species=customer.pet_species,
                    service_id=petservice1.service_id
                )
            )
            return petservice1
        except StopIteration:
            self.events.append(events.NotAvailable(customer.service_name))
            return None


@dataclass(unsafe_hash=True)
class Customer:
    customer_id: int
    service_name: str
    pet_species: str  

class PetService:
    """
	"service_id"	INTEGER NOT NULL,
	"service_name"	TEXT NOT NULL,
	"price"	INTEGER NOT NULL,
	"petSpecies"	TEXT NOT NULL,
	PRIMARY KEY("service_id" AUTOINCREMENT)
    """
    def __init__(self,service_name: str,price: int,pet_species: str):
        #self.service_id = service_id,
        self.service_name = service_name
        self.price = price
        self.pet_species = pet_species
        self._allocations = set()

    def allocate(self, customer: Customer):
        if self.can_allocate(customer):
            self._allocations.add(customer)

    def can_allocate(self, customer: Customer) -> bool:
        return self.service_name == customer.service_name and self.pet_species == customer.pet_species

