import pandas as pd

from dao.reader.base import BaseProjectionsReader
from model.kind import ReaderKind
from model.season import Season


class SteveLaidlawReader(BaseProjectionsReader):

    seasons = [
        Season.SEASON_2023_2024, 
        Season.SEASON_2024_2025, 
    ]

    def __init__(self, filename: str, season: Season, rank_col='Rank'):
        super().__init__(
            kind=ReaderKind.PROJECTION, 
            filename=filename, 
            season=season,
            primary_col="Name", 
            rank_col=rank_col, 
            position_col='N/A', 
            sheet_name="Skaters Rankings"
        )
        self.weight = 75

    def find_by_rgx(self, filter_regex: str):
        return super().find_by_rgx(filter_regex)[[
            self.rank_col,
            self.primary_col,
            'GP',
            'G',
            'A',
            'P',
            'PPP',
            'SOG',
            'Hits',
            'Blks'
        ]]
