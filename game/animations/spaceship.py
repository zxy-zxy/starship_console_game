import asyncio
import itertools

from curses_tools import draw_frame
from physics import update_speed

from animations.yamato_cannon import animate_yamato_cannon
from animations.game_over import animate_game_over

from global_variables import coroutines, obstacles
from constants import (
    SPACE_KEY_CODE,
    LEFT_KEY_CODE,
    RIGHT_KEY_CODE,
    UP_KEY_CODE,
    DOWN_KEY_CODE,
    STARSHIP_ANIMATION_ROWS,
)

starship_frame = ''
previous_starship_frame = ''


async def animate_spaceship():
    global starship_frame
    global previous_starship_frame

    with open('frames/rocket_frame_1.txt', 'r') as f:
        starship_animation_frame_1 = f.read()

    with open('frames/rocket_frame_2.txt', 'r') as f:
        starship_animation_frame_2 = f.read()

    starship_frame_animations = [starship_animation_frame_1, starship_animation_frame_2]

    for current_starship_frame in itertools.cycle(starship_frame_animations):
        starship_frame = current_starship_frame
        await asyncio.sleep(0)
        previous_starship_frame = current_starship_frame


async def run_spaceship(canvas):
    rows_number, columns_number = canvas.getmaxyx()
    row_speed = column_speed = 0

    row = rows_number - (STARSHIP_ANIMATION_ROWS * 2)
    column = columns_number // 2

    while True:
        rows_direction, columns_direction, spase_pressed = read_controls(canvas)

        if spase_pressed:
            coroutines.append(animate_yamato_cannon(canvas, row, column))

        if (
            0 < row + rows_direction < rows_number - STARSHIP_ANIMATION_ROWS
            and 0 < column + columns_direction < columns_number
        ):

            row_speed, column_speed = update_speed(
                row_speed, column_speed, rows_direction, columns_direction
            )

            row += row_speed
            column += column_speed

            draw_frame(canvas, row, column, starship_frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, previous_starship_frame, True)

            for obstacle in obstacles:
                if obstacle.has_collision(row, column):
                    coroutines.append(animate_game_over(canvas))
                    return

        else:
            await asyncio.sleep(0)


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
