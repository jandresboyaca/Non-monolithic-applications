import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import asyncio

from order.infraestructura import recibir_ordenes, almacenar_orden


async def uow():
    ordenes = await recibir_ordenes()
    almacenar_orden(ordenes)


if __name__ == '__main__':
    asyncio.run(uow())
