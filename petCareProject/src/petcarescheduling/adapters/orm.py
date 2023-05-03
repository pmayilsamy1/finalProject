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
from sqlalchemy.orm import  registry,mapper, relationship

from petcarescheduling.domain import models

mapper_registry = registry()
Base = mapper_registry.generate_base()


logger = logging.getLogger(__name__)

metadata = mapper_registry.metadata

petServices = Table(
   "petservice",
    metadata,
    Column("service_id", Integer, primary_key=True, autoincrement=True),
    Column("service_name", ForeignKey("service.service_name")),
    Column("price", Integer),
    Column("pet_species", String(255)),
    Column("qty", Integer)
   
)

'''CREATE TABLE "customer_table" (
	"id"	INTEGER NOT NULL,
	"pet_species"	TEXT NOT NULL,
	"service_name"	TEXT NOT NULL,
	"customer_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
)'''
customer_table = Table(
    "customer_table",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("service_name", String(255),nullable=False),
    Column("pet_species", String(255), nullable=False),
    Column("customer_id", Integer),
    Column("qty",Integer)
)

'''CREATE TABLE "allocate_service" (
	"id"	INTEGER NOT NULL,
	"customer_id"	INTEGER NOT NULL,
	"service_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
	FOREIGN KEY ("customer_id") REFERENCES customer_table("customer_id")
	FOREIGN KEY("service_id") REFERENCES petservice("service_id")
)'''
allocations = Table(
    "allocate_service",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("customer_id", ForeignKey("customer_table.customer_id")),
    Column("service_id", ForeignKey("petservice.service_id")),
)

service = Table(
    "service",
    metadata,
    Column("service_name", String(255), primary_key=True),
    Column("version_number", Integer, nullable=False, server_default="0"),
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
    logger.info("Starting mappers")
    customer_mapper = mapper_registry.map_imperatively(models.Customer, customer_table)
    petservice_mapper = mapper_registry.map_imperatively(
        models.PetService,
        petServices,
        properties={
            "_allocations": relationship(
                customer_mapper,
                secondary=allocations,
                collection_class=set,
            )
        },
    )
    mapper_registry.map_imperatively(
        models.Service,
        service,
        properties={"petservices": relationship(petservice_mapper)},
    )

@event.listens_for(models.Service, "load")
def receive_load(service, _):
    service.events = []