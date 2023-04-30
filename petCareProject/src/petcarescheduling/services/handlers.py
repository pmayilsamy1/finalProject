#add service
#update service
#delete service
#list all services

from __future__ import annotations
from dataclasses import asdict
from typing import List, Dict, Callable, Type, TYPE_CHECKING
from petcarescheduling.domain import commands, events, models
import logging

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from petcarescheduling.adapters import notifications
    from . import unit_of_work

class InvalidService(Exception):
    pass

def add_service(
    cmd: commands.CreateService,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        # look to see if we already have this bookmark as the title is set as unique
        service = uow.services.get(service_name=cmd.service_name)
        if service is None:
            print("Inside if")
            print(cmd.service_name,cmd.price,cmd.pet_species)

            service = models.Service(cmd.service_name, petservices=[])
            uow.services.add(service)
        service.petservices.append(models.PetService(cmd.service_name, cmd.price,cmd.pet_species))
        uow.commit()

def allocate(
    cmd: commands.AllocateService,
    uow: unit_of_work.AbstractUnitOfWork,
):
    print(cmd.customer_id, cmd.service_name, cmd.pet_species)
    customer = models.Customer(cmd.customer_id, cmd.service_name, cmd.pet_species)
    print(customer)
    with uow:
        print("Inside with")
        service = uow.services.get(service_name=customer.service_name)
        print(service)
        if service is None:
            raise InvalidService(f"Invalid service {customer.service_name}")
        print("Not in exception")
        service.allocate(customer)
        uow.commit()

def publish_allocated_event(
    event: events.Allocated,
    publish: Callable,
):
    publish("service_allocated", event)

def send_out_of_stock_notification(
    event: events.NotAvailable,
    notifications: notifications.AbstractNotifications,
):
    notifications.send(
        "stock@made.com",
        f"Service not available for {event.service_name}",
    )


EVENT_HANDLERS = {
    
    events.Allocated: [publish_allocated_event],
    events.NotAvailable: [send_out_of_stock_notification],
    
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.CreateService: add_service,
    commands.AllocateService: allocate,
    
}  
