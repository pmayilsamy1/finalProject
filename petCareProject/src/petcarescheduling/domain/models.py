from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Set
from . import events, commands

class Service:
    def __init__(self, service_name: str, petservices: List[PetService], version_number: int = 0):
        self.service_name = service_name
        self.petservices = petservices
        self.version_number = version_number
        self.events = []  # type: List[events.Event]

    def allocate(self, customer: Customer) -> str:
        try:
            print("In allocate")
            petservice = next(b for b in sorted(self.petservices) if b.can_allocate(customer))
            petservice.allocate(customer)
            self.version_number += 1
            self.events.append(
                events.Allocated(
                    customer_id=customer.customer_id,
                    service_name=customer.service_name,
                    pet_species=customer.pet_species,
                    #service_id=petservice.service_id
                )
            )
            
            return petservice.service_name
        except StopIteration:
            self.events.append(events.NotAvailable(customer.service_name))
            return None
        
    def change_batch_quantity(self, service_name: str, qty: int):
        petservice = next(b for b in self.petservices if b.service_name == service_name)
        petservice.qty = qty
        while petservice.available_quantity < 0:
            customer = petservice.deallocate_one()
            self.events.append(events.Deallocated(customer.customer_id, customer.service_name, customer.qty))

    


@dataclass(unsafe_hash=True)
class Customer:
    customer_id: int
    service_name: str
    pet_species: str  
    qty: 1

class PetService:
    """
	"service_id"	INTEGER NOT NULL,
	"service_name"	TEXT NOT NULL,
	"price"	INTEGER NOT NULL,
	"petSpecies"	TEXT NOT NULL,
    "qty" INTEGER,
	PRIMARY KEY("service_id" AUTOINCREMENT)
    """
    def __init__(self,service_name: str,price: int,pet_species: str,quantity: int):
        #self.service_id = service_id,
        self.service_name = service_name
        self.price = price
        self.pet_species = pet_species
        self.qty = quantity
        self._allocations = set()
        

    def __repr__(self):
        return f"<PetService {self.service_name}>"

    def __eq__(self, other):
        if not isinstance(other, PetService):
            return False
        return other.reference == self.service_name

    def __hash__(self):
        return hash(self.service_name)

    def allocate(self, customer: Customer):
        if self.can_allocate(customer):
            self._allocations.add(customer)
    
    def deallocate_one(self) -> Customer:
        return self._allocations.pop()
    

    @property
    def allocated_quantity(self) -> int:
        return sum(customer.qty for customer in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self.qty - self.allocated_quantity

    def can_allocate(self, customer: Customer) -> bool:
        print(self.available_quantity,customer.qty)
        decision = self.service_name == customer.service_name and self.pet_species == customer.pet_species and int(self.available_quantity) >= int(customer.qty)
        print(decision)
        return decision

