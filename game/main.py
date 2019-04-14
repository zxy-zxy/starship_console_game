import random
import time
import curses

from animations.garbage import fill_orbit_with_garbage
from animations.blink import animate_blink
from animations.spaceship import animate_spaceship, run_spaceship

from obstacles import show_obstacles
from timeline import increment_year

from constants import TIC_TIMEOUT, STARS_QUANTITY

from global_variables import coroutines, obstacles


def initialize_coroutines(canvas):
    star_symbols = ['+', '*', '.', ':']

    rows_number, columns_number = canvas.getmaxyx()

    stars_to_canvas = [
        (
            random.randint(0, rows_number - 1),
            random.randint(0, columns_number - 1),
            random.choice(star_symbols),
        )
        for _ in range(STARS_QUANTITY)
    ]

    for star in stars_to_canvas:
        coroutines.append(animate_blink(canvas, *star))

    coroutines.append(increment_year(canvas))

    coroutines.append(run_spaceship(canvas))
    coroutines.append(animate_spaceship())
    coroutines.append(fill_orbit_with_garbage(canvas))
    coroutines.append(show_obstacles(canvas, obstacles))

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
