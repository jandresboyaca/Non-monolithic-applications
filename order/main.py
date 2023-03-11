import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import asyncio

from order.infraestructura import uow, almacenar_orden, crear_evento, crear_log


async def main():
    await uow(
        almacenar_orden=almacenar_orden,
        crear_evento=crear_evento,
        crear_log=crear_log
    )

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
