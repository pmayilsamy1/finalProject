#add service
#update service
#delete service
#list all services

from __future__ import annotations

from typing import List, Dict, Callable, Type, TYPE_CHECKING
from petcarescheduling.domain import commands, events, models
import logging

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from petcarescheduling.adapters import notifications
    from . import unit_of_work


def add_service(
    cmd: commands.CreateService,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        # look to see if we already have this bookmark as the title is set as unique
        service = uow.petservices.get(service_name=cmd.service_name)
        if service is None:
            print("Inside if")
            print(cmd.service_name,cmd.price,cmd.pet_species)

            service = models.PetService(str(cmd.service_name),int(cmd.price),str(cmd.pet_species))
            uow.petservices.add(service)
        else: 
            print("Already available")
        uow.commit()


EVENT_HANDLERS = {
    events.PetServiceAdded: [add_service],
    
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.CreateService: add_service,
    
}  
