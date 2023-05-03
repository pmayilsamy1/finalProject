from abc import ABC
from dataclasses import dataclass


class Event(ABC):
    pass

@dataclass
class Allocated(Event):
    customer_id: int
    service_name: str
    pet_species: str
    #service_id: int

@dataclass
class Deallocated(Event):
    customer_id: str
    service_name: str
    qty: int


@dataclass
class NotAvailable(Event):
    service_name: str
    
