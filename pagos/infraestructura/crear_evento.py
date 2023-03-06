import os
import logging
import uuid
import pulsar

from schemas.transaccion_procesada_pb2 import TransaccionProcesada

logger = logging.getLogger('pagos:event')
logger.setLevel(logging.DEBUG)
consola = logging.StreamHandler()
consola.setLevel(logging.DEBUG)
logger.addHandler(consola)

service_id = str(uuid.uuid4())


def crear_evento(order, transaction):
    logger.info("Crear evento %s, %s", order, transaction)
    client = pulsar.Client(os.environ.get('PULSAR_BROKER_URL'))

    producer = client.create_producer('transaccion-creada')
    event = TransaccionProcesada()
    event.order_id = order.id
    event.status = transaction["status"]
    logger.info(event)
    event_bytes = event.SerializeToString()
    producer.send(event_bytes)

    client.close()
