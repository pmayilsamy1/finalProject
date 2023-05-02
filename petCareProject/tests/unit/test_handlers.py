# pylint: disable=no-self-use
from __future__ import annotations
from collections import defaultdict
from typing import Dict, List
import pytest
from petcarescheduling import bootstrap
from petcarescheduling.domain import commands
from petcarescheduling.services import handlers
from petcarescheduling.adapters import notifications, repository
from petcarescheduling.services import unit_of_work

class FakeRepository(repository.AbstractPetServicesRepository):
    def __init__(self, services):
        super().__init__()
        self._services = set(services)

    def _add(self, services):
        self._services.add(services)

    def _get(self, service_name):
        return next((p for p in self._services if p.service_name == service_name), None)

    def _get_by_batchref(self, batchref):
        return next(
            (p for p in self._services for b in p.service if b.reference == batchref),
            None,
        )
    
class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.services = FakeRepository([])
        self.committed = False

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass

class FakeNotifications(notifications.AbstractNotifications):
    def __init__(self):
        self.sent = defaultdict(list)  # type: Dict[str, List[str]]

    def send(self, destination, message):
        self.sent[destination].append(message)

def bootstrap_test_app():
    return bootstrap.bootstrap(
        start_orm=False,
        uow=FakeUnitOfWork(),
        notifications=FakeNotifications(),
        publish=lambda *args: None,
    )

class TestAddPetService:
    def test_for_new_petservice(self):
        bus = bootstrap_test_app()
        bus.handle(commands.CreateService("HairCut",50,"GoldenDoodle"))
        assert bus.uow.services.get("HairCut") is not None
        assert bus.uow.committed

    def test_for_existing_petservice(self):
        bus = bootstrap_test_app()
        bus.handle(commands.CreateService("HairCut",50,"GoldenDoodle"))
        bus.handle(commands.CreateService("HairCut",50,"GoldenDoodle"))
        assert "HairCut" in [
            b.service_name for b in bus.uow.services.get("HairCut").petservices
        ]

