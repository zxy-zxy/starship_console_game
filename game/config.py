SHOW_OBSTACLES_BORDERS = False

STARS_QUANTITY = 50

SPACESHIP_ANIMATIONS_ROWS = 10
SPACESHIP_ANIMATIONS_COLUMNS = 5
TRASH_ANIMATION_COLUMNS = 13

TIC_TIMEOUT = 0.1
TICS_PER_YEAR = 5
GAME_YEAR_BEGINNING = 1957
YAMATO_GUN_AVAILABLE_SINCE_YEAR = 2020

INFO_CANVAS_ROW_HEIGHT = 3

GARBAGE_ANIMATIONS_FILE_PATHS = [
    'frames/trash_large.txt',
    'frames/trash_small.txt',
    'frames/hubble.txt',
    'frames/duck.txt',
    'frames/lamp.txt',
]

SPACESHIP_ANIMATIONS_FILEPATHS = [
    'frames/rocket_frame_1.txt',
    'frames/rocket_frame_2.txt',
]

PHRASES = {
    1957: "First Sputnik",
    1961: "Gagarin flew!",
    1969: "Armstrong got on the moon!",
    1971: "First orbital space station Salute-1",
    1981: "Flight of the Shuttle Columbia",
    1998: 'ISS start building',
    2011: 'Messenger launch to Mercury',
    2020: "Yamato cannon is charged! Shoot the garbage!",
}


def get_garbage_delay_tics(year):
    if year < 1961:
        return 25
    elif year < 1969:
        return 20
    elif year < 1981:
        return 14
    elif year < 1995:
        return 10
    elif year < 2010:
        return 8
    elif year < 2020:
        return 6
    else:
        return 2
