import logging
import os
import sys

from pulsar import Client, ConsumerType

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import asyncio

from order.infraestructura import recibir_ordenes
logger = logging.getLogger('test')
logger.setLevel(logging.DEBUG)
consola = logging.StreamHandler()
consola.setLevel(logging.DEBUG)
logger.addHandler(consola)

async def uow():
    client = Client(os.environ.get('PULSAR_BROKER_URL'))
    consumer = client.subscribe(
        topic="orden-creada",
        subscription_name="my-subscription", ## Random Here
        consumer_type=ConsumerType.Shared
    )
    await recibir_ordenes(consumer,logger)
    #almacenar_orden(ordenes)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(uow())
