import os
import logging
import uuid
import pulsar

from schemas.orden_creada_pb2 import OrdenCreada

logger = logging.getLogger('evento:client')
logger.setLevel(logging.DEBUG)
consola = logging.StreamHandler()
consola.setLevel(logging.DEBUG)
logger.addHandler(consola)

service_id = str(uuid.uuid4())


def crear_evento(order):
    logger.info("Crear evento %s", str(order.id))
    client = pulsar.Client(os.environ.get('PULSAR_BROKER_URL'))

    producer = client.create_producer('orden-creada')
    event = OrdenCreada()
    event.id = order.id
    event.client_id = order.client_id
    event.address = order.address
    event.status = order.status
    event.created_at = order.created_at
    event.service = service_id
    logger.info(event)
    event_bytes = event.SerializeToString()
    producer.send(event_bytes)

    client.close()
