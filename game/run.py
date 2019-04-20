import random
import time
import curses

from animations.garbage import fill_orbit_with_garbage
from animations.blink import animate_blink
from animations.spaceship import animate_spaceship, run_spaceship

from obstacles import show_obstacles
from config import (
    TIC_TIMEOUT,
    STARS_QUANTITY,
    SHOW_OBSTACLES_BORDERS,
    INFO_CANVAS_ROW_HEIGHT
)
from global_variables import coroutines, obstacles, game_time_line


def initialize_coroutines(game_canvas, info_canvas):
    star_symbols = ['+', '*', '.', ':']

    rows_number, columns_number = game_canvas.getmaxyx()

    stars_to_canvas = [
        (
            random.randint(0, rows_number - 1),
            random.randint(0, columns_number - 1),
            random.choice(star_symbols),
        )
        for _ in range(STARS_QUANTITY)
    ]

    for star in stars_to_canvas:
        coroutines.append(animate_blink(game_canvas, *star))

    coroutines.append(game_time_line.increment_year())
    coroutines.append(game_time_line.show_year(info_canvas))
    coroutines.append(run_spaceship(game_canvas))
    coroutines.append(animate_spaceship())
    coroutines.append(fill_orbit_with_garbage(game_canvas))

    if SHOW_OBSTACLES_BORDERS:
        coroutines.append(show_obstacles(game_canvas, obstacles))

    return coroutines


def main(canvas):
    rows_number, columns_number = canvas.getmaxyx()

    info_canvas = canvas.derwin(INFO_CANVAS_ROW_HEIGHT, columns_number, 0, 0)
    info_canvas.border()

    game_canvas = canvas.derwin(
        rows_number - INFO_CANVAS_ROW_HEIGHT,
        columns_number,
        INFO_CANVAS_ROW_HEIGHT,
        0
    )
    game_canvas.keypad(True)
    game_canvas.nodelay(True)

    curses.curs_set(False)

    coroutines = initialize_coroutines(game_canvas, info_canvas)

    while coroutines:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        game_canvas.refresh()
        info_canvas.refresh()

        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
