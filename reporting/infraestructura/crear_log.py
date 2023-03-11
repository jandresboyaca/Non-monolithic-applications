import os
import logging
import uuid
import pulsar

from schemas.crear_log_pb2 import CrearLog

logger = logging.getLogger('order:saga_log')
logger.setLevel(logging.DEBUG)
consola = logging.StreamHandler()
consola.setLevel(logging.DEBUG)
logger.addHandler(consola)

service_id = str(uuid.uuid4())


def crear_log(orden):
    logger.info("Crear evento %s", str(orden.id))
    client = pulsar.Client(os.environ.get('PULSAR_BROKER_URL'))

    producer = client.create_producer("crear-log")
    command = CrearLog()
    command.id = orden.id
    command.entidad = "reporte"
    command.estado = orden.status
    command.created_at = orden.created_at
    logger.info(command)
    event_bytes = command.SerializeToString()
    producer.send(event_bytes)

    client.close()
