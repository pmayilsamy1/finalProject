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

    @abc.abstractmethod
    def _add(self, service: models.Service):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, service_name) -> models.Service:
        raise NotImplementedError

class SqlAlchemyPetServicesRepository(AbstractPetServicesRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session


    def _add(self, service):
        self.session.add(service)

    def _get(self, service_name):
        return self.session.query(models.Service).filter_by(service_name=service_name).first()

    def _get_by_batchref(self, service_name):
        return (
            self.session.query(models.Service)
            .join(models.PetService)
            .filter(
                orm.petService.c.reference == service_name,
            )
            .first()
        )
    
