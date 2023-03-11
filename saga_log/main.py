import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import asyncio

from saga_log.infraestructura import uow


async def main():
    await uow()


if __name__ == '__main__':
    asyncio.run(main())
