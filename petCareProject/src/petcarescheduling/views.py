from petcarescheduling.services import unit_of_work
from sqlalchemy.sql import text


def allocations(customerid: int, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        query = text("SELECT id,customer_id,service_name, pet_species FROM customer_table WHERE customer_id = :customer_id")
        results = uow.session.execute(query,dict(customer_id=customerid))
    
        return  [dict(r._mapping) for r in results]
    