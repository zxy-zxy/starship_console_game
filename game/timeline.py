from tools import sleep, Singleton

from config import GAME_YEAR_BEGINNING, TICS_PER_YEAR


class Timeline(metaclass=Singleton):
    def __init__(self, year, tics_per_year):
        self.tics_per_year = tics_per_year
        self.year = year

    async def increment_year(self):
        while True:
            await sleep(self.tics_per_year)
            self.year += 1


game_time_line = Timeline(GAME_YEAR_BEGINNING, TICS_PER_YEAR)
