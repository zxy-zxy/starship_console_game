import asyncio
import random
import curses


async def blink(canvas, row, column, symbol='*'):
    while True:

        canvas.addstr(row, column, symbol, curses.A_DIM)
        for i in range(random.randint(0, 20)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(random.randint(0, 3)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for i in range(random.randint(0, 5)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(random.randint(0, 3)):
            await asyncio.sleep(0)
