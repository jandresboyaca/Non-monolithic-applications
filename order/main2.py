import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import asyncio

from order.infraestructura import uow2, actualizar_orden, crear_evento


async def main():
    await uow2(actualizar_orden=actualizar_orden, crear_evento=crear_evento)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
