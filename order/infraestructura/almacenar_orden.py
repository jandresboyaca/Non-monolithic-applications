import logging
import os

from sqlalchemy_orm import Model, Database
from datetime import datetime
import uuid

Base = Model()

logger = logging.getLogger('db:order')
logger.setLevel(logging.DEBUG)
consola = logging.StreamHandler()
consola.setLevel(logging.DEBUG)
logger.addHandler(consola)


class Orden(Base):
    id: str
    message_id: str
    client_id: int
    address: str
    status: str
    created_at: datetime


db = Database(os.environ.get('POSTGRES_URL'))
db.create(Orden)


def almacenar_orden(orden):
    logger.info("Almacenando orden %s", str(orden.id))
    session = db.session()
    db_orden = Orden(
        id=str(uuid.uuid4()),
        message_id=str(orden.id),
        client_id=orden.client_id,
        address=orden.address,
        status=orden.status,
        created_at=datetime.fromtimestamp(orden.created_at)
    )
    session.create(db_orden)
    session.commit()
