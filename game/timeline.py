import asyncio

from global_variables import year
from game_scenario import PHRASES
from tools import sleep


async def increment_year(canvas):
    global year
    while True:
        new_phrase = PHRASES.get(year[0])
        if new_phrase:
            phrase = new_phrase
            message = str(year[0]) + ' ' + phrase
        else:
            message = str(year[0]) + ' ' + phrase
        canvas.addstr(2, 10, message)
        await sleep(10)
        year[0] += 1
