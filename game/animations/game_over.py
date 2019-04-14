import asyncio
from curses_tools import draw_frame


async def animate_game_over(canvas):
    rows_number, columns_number = canvas.getmaxyx()
    with open('frames/game_over.txt') as f:
        game_over_text = f.read()
    while True:
        draw_frame(canvas, rows_number // 3, columns_number // 3, game_over_text)
        await asyncio.sleep(0)
