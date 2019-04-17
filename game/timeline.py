from tools import sleep, Singleton
from curses_tools import draw_frame

from config import GAME_YEAR_BEGINNING, TICS_PER_YEAR, PHRASES


class Timeline(metaclass=Singleton):
    def __init__(self, year, tics_per_year):
        self.tics_per_year = tics_per_year
        self.year = year

    async def increment_year(self):
        while True:
            await sleep(self.tics_per_year)
            self.year += 1

    async def show_year(self, canvas):
        phrase, previous_phrase = '', ''

        while True:
            phrase = PHRASES.get(self.year, '')
            if phrase:
                previous_phrase = phrase
            text = f'{self.year} - {phrase}' if phrase else f'{self.year} - {previous_phrase}'
            draw_frame(canvas, 1, 2, text)
            await sleep(1)
            draw_frame(canvas, 1, 2, text, negative=True)


game_time_line = Timeline(GAME_YEAR_BEGINNING, TICS_PER_YEAR)
