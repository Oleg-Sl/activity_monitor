#!/usr/bin/env python

import os
import sys
import asyncio
from pprint import pprint

from app.db.db import get_async_session


async def main() -> None:
    db = next(get_async_session())
    



if __name__ == "__main__":
    asyncio.run(main())
