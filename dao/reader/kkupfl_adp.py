import pandas as pd

from dao.reader.base import BaseProjectionsReader
from model.kind import ReaderKind
from model.season import Season


class KKUPFLAdpReader(BaseProjectionsReader):

    seasons = [
        Season.SEASON_2023_2024,
        Season.SEASON_2024_2025
    ]

    def __init__(self, filename: str, season: Season):
        super().__init__(
            kind=ReaderKind.PROJECTION, 
            filename=filename, 
            season=season,
            primary_col='Player', 
            rank_col='Full MOCK ADP ', 
            position_col='POS'
        )
        self.weight = 75

    def find_by_rgx(self, filter_regex: str):
        return super().find_by_rgx(filter_regex)[[
            self.rank_col,
            self.primary_col,
            self.position_col,
            'POS Rank',
            'Count',
            'Min',
            'Max',
            'Variance',
        ]]
