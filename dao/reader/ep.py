import pandas as pd

from dao.reader.base import BaseProjectionsReader
from model import season
from model.kind import ReaderKind
from model.season import Season


class EliteProspectsReader(BaseProjectionsReader):

    seasons = [
        Season.SEASON_2023_2024,
        Season.SEASON_2024_2025
    ]

    def __init__(self, filename: str, season: Season, rank_col='Rank'):
        super().__init__(
            kind=ReaderKind.PROJECTION,
            filename=filename,
            season=season,
            primary_col="Name",
            rank_col=rank_col,
            position_col='Pos',
            team_col="Team"
        )
        self.weight = 75

    def query_primary_col(self, query: str, limit: int = -1):
        return super().query_primary_col(query, limit)[[
            self.rank_col,
            self.primary_col,
            self.position_col,
            'Team',
            'Points',
            'Games',
            'Goals',
            'Assists'
        ]]
