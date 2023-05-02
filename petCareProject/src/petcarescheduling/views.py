from petcarescheduling.services import unit_of_work


def allocations(customer_id: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        results = uow.session.execute(
            """
            SELECT sku, batchref FROM allocations_view WHERE orderid = :orderid
            """,
            dict(customer_id=customer_id),
        )
    return [dict(r) for r in results]
