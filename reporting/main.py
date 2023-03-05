import asyncio
import os
import uuid

from pulsar import Client, ConsumerType

from reporting.infraestructura import on_orden_created


async def uow():
    client = Client(os.environ.get('PULSAR_BROKER_URL'))
    consumer = client.subscribe(
        topic="orden-creada",
        subscription_name="reporting " + str(uuid.uuid4()),
        consumer_type=ConsumerType.Shared
    )
    await on_orden_created(consumer)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(uow())
