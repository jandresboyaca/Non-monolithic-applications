import logging
import os
from datetime import datetime

from pulsar import Client, ConsumerType

from schemas.crear_log_pb2 import CrearLog


class LoggerNameFilter(logging.Filter):
    def filter(self, record):
        record.logger_name = record.name
        return True


pulsar_logger = logging.getLogger('pulsar')
pulsar_logger.setLevel(logging.WARNING)

saga_logger = logging.getLogger('saga_log')
saga_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('./saga_log/order.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s; %(message)s')
file_handler.setFormatter(formatter)
saga_logger.addHandler(file_handler)

logger = logging.getLogger('saga_log:console')
logger.setLevel(logging.DEBUG)
consola = logging.StreamHandler()
consola.setLevel(logging.DEBUG)
logger.addHandler(consola)


async def uow():
    client = Client(os.environ.get('PULSAR_BROKER_URL'), logger=pulsar_logger)
    consumer = client.subscribe(
        topic="crear-log",
        subscription_name="my-subscription",
        consumer_type=ConsumerType.Shared
    )
    while True:
        try:
            msg = consumer.receive()
            command = CrearLog()
            command.ParseFromString(msg.data())
            saga_logger.info("%s; %s; %s; %s" % (command.id, command.entidad, command.estado, datetime.fromtimestamp(command.created_at)))
            logger.info("%s; %s; %s; %s" % (command.id, command.entidad, command.estado, datetime.fromtimestamp(command.created_at)))
            consumer.acknowledge(msg)
        except Exception as e:
            saga_logger.error("Failed to process message with ID  %s" % (e))
