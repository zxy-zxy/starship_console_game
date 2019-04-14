import asyncio
import random

from obstacles import Obstacle
from curses_tools import draw_frame, get_frame_size
from tools import sleep

from animations.explosion import animate_explosion

from game_scenario import get_garbage_delay_tics
from constants import TRASH_ANIMATION_COLUMNS
from global_variables import (
    coroutines,
    obstacles,
    obstacles_in_last_collisions, year
)


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0
    garbage_row_size, garbage_column_size = get_frame_size(garbage_frame)
    obstacle = Obstacle(row, column, garbage_row_size, garbage_column_size)
    obstacles.append(obstacle)

    try:
        while row < rows_number:
            if obstacle in obstacles_in_last_collisions:
                obstacles_in_last_collisions.remove(obstacle)
                break
            draw_frame(canvas, row, column, garbage_frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, garbage_frame, negative=True)
            row += speed
            obstacle.row = row
    finally:
        obstacles.remove(obstacle)
        await animate_explosion(canvas, row, column)
        return


async def fill_orbit_with_garbage(canvas):
    rows_number, columns_number = canvas.getmaxyx()

    garbage_animations = list()

    with open('frames/trash_large.txt') as f:
        trash_large_animation = f.read()
        garbage_animations.append(trash_large_animation)

    with open('frames/trash_small.txt') as f:
        trash_small_animation = f.read()
        garbage_animations.append(trash_small_animation)

    with open('frames/hubble.txt') as f:
        hubble = f.read()
        garbage_animations.append(hubble)

    with open('frames/duck.txt') as f:
        duck = f.read()
        garbage_animations.append(duck)

    with open('frames/lamp.txt') as f:
        lamp = f.read()
        garbage_animations.append(lamp)

    while True:
        animation_to_appear = random.choice(garbage_animations)
        column_at_appear = random.randint(1, columns_number - TRASH_ANIMATION_COLUMNS)
        coroutines.append(fly_garbage(canvas, column_at_appear, animation_to_appear))
        # delay_tics = get_garbage_delay_tics(year)
        await sleep(20)
