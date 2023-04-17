import abc
from typing import Set
from petcarescheduling.domain import models



class AbstractPetServicesRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.Product]

    def add(self, petservice: models.PetService):
        self._add(petservice)
        self.seen.add(petservice)

    def get(self, service_name) -> models.PetService:
        petservice = self._get(service_name)
        if petservice:
            self.seen.add(petservice)
        return petservice


    @abc.abstractmethod
    def _add(self, petservice: models.PetService):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, service_name) -> models.PetService:
        raise NotImplementedError

class SqlAlchemyPetServicesRepository(AbstractPetServicesRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session


    def _add(self, petservice):
        self.session.add(petservice)

    def _get(self, service_name):
        return self.session.query(models.PetService).filter_by(service_name=service_name).first()
