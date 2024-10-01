import pandas as pd

from model.kind import ReaderKind
from dao.reader.base import BaseProjectionsReader
from model.season import Season


class BlakeRedditReader(BaseProjectionsReader):

    seasons = [ Season.SEASON_2024_2025 ]

    def __init__(self, filename: str, season: Season, rank_col='Rank', primary_col="Name"):
        super().__init__(
            kind=ReaderKind.PROJECTION, 
            filename=filename, 
            season=season,
            primary_col=primary_col, 
            rank_col=rank_col, 
            position_col='Pos', 
            sheet_name="Skaters Trimmed"
        )
        self.weight = 75

    def get_by_rgx(self, filter_regex: str):
        return super().get_by_rgx(filter_regex)[[
            self.rank_col,
            self.primary_col,
            'Proj Pos',
            self.position_col,
            'FPTS per GP',
            'PTS',
            'G',
            'A',
            'GP',

            'PPP',
            'SOG',
            'HIT',
            'BLK',
            'S%',
            'ATOI',
        ]]
