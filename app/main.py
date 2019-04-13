import asyncio
import random
import time
import curses

from fire_animation import fire
from blink_animation import blink
from starship_animation import starship
from curses_tools import draw_frame
from asyncio_tools import sleep

from constants import TIC_TIMEOUT, STARS_QUANTITY, STARSHIP_ANIMATION_ROWS, TRASH_ANIMATION_COLUMNS

coroutines = list()


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def fill_orbit_with_garbage(canvas):
    rows_number, columns_number = canvas.getmaxyx()

    garbage_animations = list()

    with open('frames/trash_large.txt') as f:
        trash_large_animation = f.read()
        garbage_animations.append(trash_large_animation)

    with open('frames/trash_small.txt') as f:
        trash_small_animation = f.read()
        garbage_animations.append(trash_small_animation)

    while True:
        animation_to_appear = random.choice(garbage_animations)
        column_at_appear = random.randint(1, columns_number - TRASH_ANIMATION_COLUMNS)
        coroutines.append(fly_garbage(canvas, column_at_appear, animation_to_appear))
        await sleep(20)


def initialize_coroutines(canvas):
    star_symbols = ['+', '*', '.', ':']

    rows_number, columns_number = canvas.getmaxyx()

    stars_to_canvas = [
        (
            random.randint(0, rows_number - 1),
            random.randint(0, columns_number - 1),
            random.choice(star_symbols)) for _ in range(STARS_QUANTITY)
    ]

    for star in stars_to_canvas:
        coroutines.append(blink(canvas, *star))

    with open('frames/rocket_frame_1.txt', 'r') as f:
        startship_animation_1 = f.read()

    with open('frames/rocket_frame_2.txt', 'r') as f:
        startship_animation_2 = f.read()

    starship_initial_row_position = rows_number - (STARSHIP_ANIMATION_ROWS * 2)
    starship_initial_column_position = columns_number // 2

    coroutines.append(starship(canvas, starship_initial_row_position, starship_initial_column_position,
                               [startship_animation_1, startship_animation_2]))

    coroutines.append(fire(canvas, starship_initial_row_position, starship_initial_column_position))

    coroutines.append(fill_orbit_with_garbage(canvas))

    return coroutines


def main(canvas):
    canvas.nodelay(True)
    curses.curs_set(False)

    coroutines = initialize_coroutines(canvas)

    while coroutines:
        try:
            for coroutine in coroutines:
                coroutine.send(None)

            canvas.refresh()

            time.sleep(TIC_TIMEOUT)

        except StopIteration:
            coroutines.remove(coroutine)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
