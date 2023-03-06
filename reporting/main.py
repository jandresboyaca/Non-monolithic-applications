import asyncio
import os
import uuid
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from pulsar import Client, ConsumerType

from reporting.infraestructura import on_orden_created


async def uow():
    client = Client(os.environ.get('PULSAR_BROKER_URL'))
    consumer = client.subscribe(
        topic="orden-actualizada",
        subscription_name="reporting " + str(uuid.uuid4()),
        consumer_type=ConsumerType.Shared
    )
    await on_orden_created(consumer)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(uow())
