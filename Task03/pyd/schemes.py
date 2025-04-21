from .base_models import *
from typing import List

class GenreSchema(BaseGenre):
    films: List[BaseFilm]


class FilmSchema(BaseFilm):
    genres: List[BaseGenre]