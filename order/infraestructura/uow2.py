import logging
import os
from pulsar import Client, ConsumerType

from schemas.transaccion_procesada_pb2 import TransaccionProcesada

logger = logging.getLogger('uow2:order')
logger.setLevel(logging.DEBUG)
consola = logging.StreamHandler()
consola.setLevel(logging.DEBUG)
logger.addHandler(consola)


async def uow2(**kwargs):
    client = Client(os.environ.get('PULSAR_BROKER_URL'))
    consumer = client.subscribe(
        topic="transaccion-creada",
        subscription_name="my-subscription",
        consumer_type=ConsumerType.Shared
    )
    while True:
        try:
            msg = consumer.receive()
            command = TransaccionProcesada()
            command.ParseFromString(msg.data())
            logger.info("Received transaccion-creada with ID %s: %s" % (msg.message_id(), command))
            order = None
            for key, step in kwargs.items():
                if key == "actualizar_orden":
                    order = step(command)
                if key == "crear_evento":
                    step(order, "orden-actualizada")
                if key == "crear_log":
                    step(order, "orden actualiazada")
            consumer.acknowledge(msg)
        except Exception as e:
            logger.info("Failed to process message with ID  %s" % (e))
