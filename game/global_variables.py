from timeline import Timeline
from config import GAME_YEAR_BEGINNING, TICS_PER_YEAR

coroutines = list()
obstacles = list()
obstacles_in_last_collisions = list()

game_time_line = Timeline(GAME_YEAR_BEGINNING, TICS_PER_YEAR)
