import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import pulsar

from schemas.orden_pb2 import Orden


def create_order():
    try:
        client = pulsar.Client('pulsar://pulsar-broker:6650')

        producer = client.create_producer('crear-orden')

        event = Orden()
        event.id = "999989"
        event.client_id = 1
        event.address = "cll falsa 123"
        event.status = "pending"

        event_bytes = event.SerializeToString()

        producer.send(event_bytes)

        # producer.close()
        # client.close()
    except pulsar.ClientConnectionError as e:
        print(f"Failed to connect to Pulsar broker: {e}")


if __name__ == '__main__':
    create_order()
