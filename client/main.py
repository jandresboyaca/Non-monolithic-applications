import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import pulsar

from schemas.orden_pb2 import Orden


def create_order():
    client = pulsar.Client('pulsar://localhost:6650')

    producer = client.create_producer('orden-creada')

    event = Orden()
    event.id = "123"
    event.client_id = 1
    event.address = "cll falsa 123"
    event.status = "pending"

    event_bytes = event.SerializeToString()

    producer.send(event_bytes)

    producer.close()
    client.close()


if __name__ == '__main__':
    create_order()
