import asyncio
import random
import time
import curses

from fire_animation import fire
from blink_animation import blink
from starship_animation import starship

from constants import TIC_TIMEOUT, STARS_QUANTITY, STARSHIP_ANIMATION_ROWS


def initialize_coroutines(canvas):
    star_symbols = ['+', '*', '.', ':']

    rows_number, columns_number = canvas.getmaxyx()

    stars_to_canvas = [
        (
            random.randint(0, rows_number - 1),
            random.randint(0, columns_number - 1),
            random.choice(star_symbols)) for _ in range(STARS_QUANTITY)]

    coroutines = [
        blink(canvas, *star) for star in stars_to_canvas
    ]

    with open('rocket_frame_1.txt', 'r') as f:
        startship_animation_1 = f.read()

    with open('rocket_frame_2.txt', 'r') as f:
        startship_animation_2 = f.read()

    starship_initial_row_position = rows_number - (STARSHIP_ANIMATION_ROWS * 2)
    starship_initial_column_position = columns_number // 2

    coroutines.append(starship(canvas, starship_initial_row_position, starship_initial_column_position,
                               [startship_animation_1, startship_animation_2]))

    coroutines.append(fire(canvas, starship_initial_row_position, starship_initial_column_position))

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
