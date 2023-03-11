import logging

from .almacenar_orden import create_report
from .crear_log import crear_log
from schemas.orden_creada_pb2 import OrdenCreada

logger = logging.getLogger('reporting-logger')
logger.setLevel(logging.DEBUG)
consola = logging.StreamHandler()
consola.setLevel(logging.DEBUG)
logger.addHandler(consola)


def on_orden_created(consumer):
    while True:
        try:
            msg = consumer.receive()
            order = OrdenCreada()
            order.ParseFromString(msg.data())
            logger.info("Received message with ID %s: %s" % (msg.message_id(), order))
            create_report(order)
            crear_log(order)
            consumer.acknowledge(msg)
        except Exception as e:
            logger.error("Failed to process message with ID  %s" % (e))
