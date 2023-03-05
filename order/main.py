import logging
import os
import sys

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
    await recibir_ordenes()
    # almacenar_orden(ordenes)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(uow())
