import logging
import os
import uuid

from sqlalchemy_orm import Model, Database
from datetime import datetime
from faker import Faker

Base = Model()

logger = logging.getLogger('db:pagos')
logger.setLevel(logging.DEBUG)
consola = logging.StreamHandler()
consola.setLevel(logging.DEBUG)
logger.addHandler(consola)

fake = Faker()
statuses = ['approved', 'rejected']


class Transaccion(Base):
    id: str
    order_id: str
    client_id: int
    value: int
    status: str
    created_at: datetime


db = Database(os.environ.get('POSTGRES_URL'))
db.create(Transaccion)


def almacenar_pago(orden):
    logger.info("Almacenando pago %s" % orden.id)
    session = db.session()
    db_transaccion = Transaccion(
        id=str(uuid.uuid4()),
        order_id=str(orden.id),
        client_id=orden.client_id,
        value=fake.random_int(min=1000, max=10000000),
        status=statuses[fake.random_int(min=0, max=1)],
        created_at=datetime.now()
    )
    transaction_dict = {"id": db_transaccion.id, "status": db_transaccion.status}
    session.create(db_transaccion)
    session.commit()
    return transaction_dict
