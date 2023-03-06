import logging

from sqlalchemy_orm import Model, Database
from .almacenar_orden import Orden, db
from schemas.orden_pb2 import Orden as ProtoOrden

Base = Model()

logger = logging.getLogger('db:order')
logger.setLevel(logging.DEBUG)
consola = logging.StreamHandler()
consola.setLevel(logging.DEBUG)
logger.addHandler(consola)


def actualizar_orden(transaction):
    logger.info("actualizar_orden orden %s", str(transaction.order_id))
    session = db.session()
    order = session.query(Orden).filter_by(message_id=str(transaction.order_id)).first()
    order.status = transaction.status
    order_proto = ProtoOrden(
        id=order.message_id,
        client_id=order.client_id,
        address=order.address,
        status=order.status,
        created_at=order.created_at.timestamp()
    )
    session.commit()
    return order_proto
