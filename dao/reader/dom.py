import pandas as pd

from dao.reader.base import BaseProjectionsReader
from model.kind import ReaderKind
from model.season import Season


class DomReader(BaseProjectionsReader):

    seasons = [
        Season.SEASON_2023_2024,
        Season.SEASON_2024_2025
    ]

    def __init__(self, filename: str, season: Season, rank_col='RK', ascending=True):
        super().__init__(
            kind=ReaderKind.PROJECTION,
            filename=filename,
            season=season,
            primary_col="NAME",
            rank_col=rank_col,
            position_col='POS',
            team_col="TEAM",
            ascending=ascending,
            sheet_name="The List"
        )
        self.weight = 700 if self.rank_col == 'RK' else 0  # don't weigh /GP rank

    def query_primary_col(self, query: str, limit: int = -1):
        return super().query_primary_col(query, limit)[[
            self.rank_col,
            self.primary_col,
            self.position_col,
            'AGE',
            'TEAM',
            'FP',
            'GP',
            'G',
            'A',
            'PTS',
            'TOI',
            'SOG',
            'BLK',
            'HIT',
            'GP.1',
            'W',
            'SV',
            'GA'
        ]]