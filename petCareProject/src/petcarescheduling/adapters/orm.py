import logging
#from typing import Text

from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
   
    String,
    Date,
    ForeignKey,
    event,
)

# from sqlalchemy.orm import mapper
from sqlalchemy.orm import registry, mapper, relationship

from petcarescheduling.domain import models

mapper_registry = registry()
Base = mapper_registry.generate_base()


logger = logging.getLogger(__name__)

metadata = mapper_registry.metadata




petService = Table(
   "petservice",
    metadata,
    Column("service_id", Integer, primary_key=True, autoincrement=True),
    Column("service_name", String(255)),
    Column("price", Integer),
    Column("pet_species", String(255)),
   
)


# def start_mappers():
#     logger.info("string mappers")
#     # SQLAlchemy 2.0
   
#     batches_mapper = mapper(
#         models.PetService,
#         petService)
#     # SQLAlchemy 1.3
#     # bookmarks_mapper = mapper(Bookmark, bookmarks)

def start_mappers():
    
    print("starting mappers")
    mapper_registry.map_imperatively(models.PetService, petService)

@event.listens_for(models.PetService, "load")
def receive_load(petservice, _):
    petservice.events = []