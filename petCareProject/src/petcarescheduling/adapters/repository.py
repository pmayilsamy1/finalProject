import abc
from typing import Set
from petcarescheduling.domain import models
from petcarescheduling.adapters import orm



class AbstractPetServicesRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.Product]

    def add(self, service: models.Service):
        self._add(service)
        self.seen.add(service)

    def get(self, service_name) -> models.Service:
        service = self._get(service_name)
        if service:
            self.seen.add(service)
        return service
    
    def get_by_service_name(self, service_name) -> models.Service:
        service = self.get_by_service_name(service_name)
        if service:
            self.seen.add(service)
        return service
    
    def updateServiceQty(self, service_name,qty) -> models.Service:
        service1 = self._getPetService(service_name)
        if(service1.qty >= qty):
            service = self._update(service_name,service1.qty - qty)
        
        

    @abc.abstractmethod
    def _add(self, service: models.Service):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, service_name) -> models.Service:
        raise NotImplementedError
    
    @abc.abstractmethod
    def _getPetService(self, service_name) -> models.PetService:
        raise NotImplementedError
    
    @abc.abstractmethod
    def _update(self, service_name,qty) -> models.Service:
        raise NotImplementedError

class SqlAlchemyPetServicesRepository(AbstractPetServicesRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session


    def _add(self, service):
        self.session.add(service)
        

    def _get(self, service_name):
        return self.session.query(models.Service).filter_by(service_name=service_name).first()
    
    def _getPetService(self, service_name):
        return self.session.query(models.PetService).filter_by(service_name=service_name).first()
    
    def _update(self, service_name,quantity):
        return self.session.query(models.PetService).filter_by(service_name=service_name).update({models.PetService.qty:quantity},synchronize_session = False)

    def _get_by_batchref(self, service_name):
        return (
            self.session.query(models.Service)
            .join(models.PetService)
            .filter(
                orm.petServices.service_name == service_name,
            )
            .first()
        )
    
