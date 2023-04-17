class PetService:
    """
	"service_id"	INTEGER NOT NULL,
	"service_name"	TEXT NOT NULL,
	"price"	INTEGER NOT NULL,
	"petSpecies"	TEXT NOT NULL,
	PRIMARY KEY("service_id" AUTOINCREMENT)
    """
    def __init__(
        self,
        service_id: int,
        service_name: str,
        price: int,
        pet_species: str
    ) -> None:
        self.service_id = service_id,
        self.service_name = service_name,
        self.price = price,
        self.pet_species = pet_species