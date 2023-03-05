import logging
import os
from pulsar import Client, Message, MessageId, ConsumerType

from schemas.orden_pb2 import Orden

logger = logging.getLogger('uow:order')
logger.setLevel(logging.DEBUG)
consola = logging.StreamHandler()
consola.setLevel(logging.DEBUG)
logger.addHandler(consola)


async def uow(**kwargs):
    client = Client(os.environ.get('PULSAR_BROKER_URL'))
    consumer = client.subscribe(
        topic="crear-orden",
        subscription_name="my-subscription",
        consumer_type=ConsumerType.Shared
    )
    while True:
        try:
            msg = consumer.receive()
            command = Orden()
            command.ParseFromString(msg.data())
            logger.info("Received message with ID %s: %s" % (msg.message_id(), command))
            for _, step in kwargs.items():
                step(command)
            consumer.acknowledge(msg)
        except Exception as e:
            logger.info("Failed to process message with ID  %s" % (e))
