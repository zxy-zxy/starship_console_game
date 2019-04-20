import asyncio
import random

from animations.explosion import animate_explosion
from obstacles import Obstacle
from curses_tools import draw_frame, get_frame_size
from tools import sleep, read_animation_from_file
from config import (
    TRASH_ANIMATION_COLUMNS,
    GARBAGE_ANIMATIONS_FILE_PATHS,
    get_garbage_delay_tics
)
from global_variables import coroutines, obstacles, obstacles_in_last_collisions, game_time_line


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 1
    garbage_row_size, garbage_column_size = get_frame_size(garbage_frame)
    obstacle = Obstacle(row, column, garbage_row_size, garbage_column_size)
    obstacles.append(obstacle)

    try:
        while row < rows_number:

            if obstacle in obstacles_in_last_collisions:
                obstacles_in_last_collisions.remove(obstacle)
                await animate_explosion(canvas, row, column)
                break

            draw_frame(canvas, row, column, garbage_frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, garbage_frame, negative=True)

            row += speed
            obstacle.row = row

    finally:
        obstacles.remove(obstacle)
        return


async def fill_orbit_with_garbage(canvas):
    rows_number, columns_number = canvas.getmaxyx()

    garbage_animations = [
        read_animation_from_file(file_path)
        for file_path in GARBAGE_ANIMATIONS_FILE_PATHS
    ]

    while True:
        delay_tics = get_garbage_delay_tics(game_time_line.year)
        animation_to_appear = random.choice(garbage_animations)
        column_at_appear = random.randint(
            1, columns_number - TRASH_ANIMATION_COLUMNS
        )
        coroutines.append(
            fly_garbage(canvas, column_at_appear, animation_to_appear)
        )
        await sleep(delay_tics)
