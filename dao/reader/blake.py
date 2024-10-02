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
            position_col='Proj Pos',
            sheet_name="Skaters Trimmed"
        )
        self.weight = 75

    def query_primary_col(self, query: str, limit: int = -1):
        return super().query_primary_col(query, limit)[[
            self.rank_col,
            self.primary_col,
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
