import asyncio
import curses

from curses_tools import draw_frame

from constants import (
    SPACE_KEY_CODE,
    LEFT_KEY_CODE,
    RIGHT_KEY_CODE,
    UP_KEY_CODE,
    DOWN_KEY_CODE,
    STARSHIP_ANIMATION_ROWS
)


async def starship(canvas, row, column, starship_animations):
    rows_number, columns_number = canvas.getmaxyx()
    while True:
        rows_direction, columns_direction, spase_pressed = read_controls(canvas)

        if 0 < row + rows_direction < rows_number - STARSHIP_ANIMATION_ROWS and 0 < column + columns_direction < columns_number:

            row += rows_direction
            column += columns_direction

            for animation in starship_animations:
                draw_frame(canvas, row, column, animation)
                await asyncio.sleep(0)
                draw_frame(canvas, row, column, animation, True)

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
