import pulsar
from _pulsar import ConsumerType

from schemas.orden_pb2 import Orden


async def recibir_ordenes():
    client = pulsar.Client('pulsar://pulsar-broker:6650')

    consumer = client.subscribe(
        topic="orden-creada",
        subscription_name="my-subscription",
        consumer_type=ConsumerType.Shared
    )
    ordenes = []
    while True:
        try:
            msg = consumer.receive()
            my_message = Orden()
            my_message.ParseFromString(msg.data())
            print("Received message with ID %s: %s" % (msg.message_id(), my_message))
            consumer.acknowledge(msg)
            ordenes.append(my_message)
            client.close()
        except Exception as e:
            print("Failed to process message with ID %s: %s" % (msg.message_id(), e))
            consumer.negative_acknowledge(msg)
            break


    return ordenes
