import os
import logging
import uuid
from datetime import datetime

import pulsar

from schemas.crear_log_pb2 import CrearLog

logger = logging.getLogger('order:saga_log')
logger.setLevel(logging.DEBUG)
consola = logging.StreamHandler()
consola.setLevel(logging.DEBUG)
logger.addHandler(consola)

service_id = str(uuid.uuid4())


def crear_log(event, transaction):
    logger.info("Crear evento %s %s", event, transaction)
    client = pulsar.Client(os.environ.get('PULSAR_BROKER_URL'))

    producer = client.create_producer("crear-log")
    command = CrearLog()
    command.id = event.id
    command.entidad = "transaccion"
    command.estado = transaction["status"]
    command.created_at = datetime.timestamp(transaction["created_at"])
    logger.info(command)
    event_bytes = command.SerializeToString()
    producer.send(event_bytes)

    client.close()
