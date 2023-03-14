import json
import logging
import os
import sys
from datetime import datetime

# Flask
from flask_restful import Resource
from google.protobuf.json_format import MessageToJson

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import pulsar
from faker import Faker

from schemas.orden_pb2 import Orden

fake = Faker()

logger = logging.getLogger('pulsar:client')
logger.setLevel(logging.DEBUG)
consola = logging.StreamHandler()
consola.setLevel(logging.DEBUG)
logger.addHandler(consola)


def get_order_data():
    dt = datetime.now()
    return {
        "id": fake.uuid4(),
        "client_id": fake.random_int(min=1, max=1000),
        "address": fake.address(),
        "status": "pending",
        "created_at": datetime.timestamp(dt)
    }


def create_order():
    try:
        client = pulsar.Client(os.environ.get('PULSAR_BROKER_URL'))

        producer = client.create_producer('crear-orden')
        command = Orden()
        order_dict = get_order_data()
        command.id = order_dict["id"]
        command.client_id = order_dict["client_id"]
        command.address = order_dict["address"]
        command.status = order_dict["status"]
        command.created_at = order_dict["created_at"]
        logger.info(command)
        event_bytes = command.SerializeToString()
        producer.send(event_bytes)

        return json.loads(MessageToJson(command))
    except pulsar.PulsarException as e:
        logger.error(f"Failed to connect to Pulsar broker: {e}")


class OrdersView(Resource):

    def post(self):

        return create_order()
