import logging
import os
from pulsar import Client, ConsumerType

from schemas.orden_creada_pb2 import OrdenCreada

logger = logging.getLogger('uow:pagos')
logger.setLevel(logging.DEBUG)
consola = logging.StreamHandler()
consola.setLevel(logging.DEBUG)
logger.addHandler(consola)


async def uow(**kwargs):
    client = Client(os.environ.get('PULSAR_BROKER_URL'))
    consumer = client.subscribe(
        topic="orden-creada",
        subscription_name="my-subscription",
        consumer_type=ConsumerType.Shared
    )
    while True:
        try:
            msg = consumer.receive()
            event = OrdenCreada()
            event.ParseFromString(msg.data())
            logger.info("Received message with ID %s: %s" % (msg.message_id(), event))
            transaction = None
            for key, step in kwargs.items():
                if key == "almacenar_pago":
                    transaction = step(event)
                if key == "crear_evento":
                    step(event, transaction)
            consumer.acknowledge(msg)
        except Exception as e:
            logger.info("Failed to process message with ID  %s" % (e))
