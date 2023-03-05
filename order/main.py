import os
import sys

from pulsar import Client, Message, MessageId, ConsumerType

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import asyncio

from order.infraestructura import recibir_ordenes, almacenar_orden


async def uow():
    client = Client('pulsar://localhost:6650')
    consumer = client.subscribe(
        topic="orden-creada",
        subscription_name="my-subscription", ## Random Here
        consumer_type=ConsumerType.Shared
    )
    await recibir_ordenes(consumer)
    #almacenar_orden(ordenes)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(uow())
