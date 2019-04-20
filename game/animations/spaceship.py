import asyncio
import itertools

from animations.yamato_cannon import animate_yamato_cannon
from animations.game_over import animate_game_over
from curses_tools import draw_frame
from physics import update_speed
from tools import read_animation_from_file
from global_variables import coroutines, obstacles, game_time_line
from config import (
    SPACESHIP_ANIMATIONS_ROWS,
    SPACESHIP_ANIMATIONS_COLUMNS,
    SPACESHIP_ANIMATIONS_FILEPATHS,
    YAMATO_GUN_AVAILABLE_SINCE_YEAR
)

SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258

spaceship_frame = ''
previous_spaceship_frame = ''


async def animate_spaceship():
    global spaceship_frame
    global previous_spaceship_frame

    spaceship_frame_animations = [
        read_animation_from_file(spaceship_animation_file_path)
        for spaceship_animation_file_path in SPACESHIP_ANIMATIONS_FILEPATHS
    ]

    for current_spaceship_frame in itertools.cycle(spaceship_frame_animations):
        spaceship_frame = current_spaceship_frame
        await asyncio.sleep(0)
        previous_spaceship_frame = current_spaceship_frame


async def run_spaceship(canvas):
    rows_number, columns_number = canvas.getmaxyx()
    row_speed = column_speed = 0

    row = rows_number - (SPACESHIP_ANIMATIONS_ROWS * 2)
    column = columns_number // 2

    while True:
        rows_direction, columns_direction, spase_pressed = read_controls(canvas)

        if spase_pressed and game_time_line.year >= YAMATO_GUN_AVAILABLE_SINCE_YEAR:
            coroutines.append(animate_yamato_cannon(canvas, row, column))

        row_speed, column_speed = update_speed(
            row_speed, column_speed, rows_direction, columns_direction
        )

        if (1 < row + row_speed < rows_number - SPACESHIP_ANIMATIONS_ROWS
                and 1 < column + column_speed < columns_number - SPACESHIP_ANIMATIONS_COLUMNS):
            row += row_speed
            column += column_speed

        draw_frame(canvas, row, column, spaceship_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, previous_spaceship_frame, True)

        for obstacle in obstacles:
            if obstacle.has_collision(row, column):
                coroutines.append(animate_game_over(canvas))
                return


def read_controls(canvas):
    """Read keys pressed and returns tuple witl controls state."""

    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed
