import pandas as pd

from dao.reader.base import BaseProjectionsReader
from model.kind import ReaderKind
from model.season import Season


class NHLReader(BaseProjectionsReader):
    """Projections from nhl.com"""

    seasons = [ Season.SEASON_2023_2024 ]

    def __init__(self, filename: str, season: Season):
        super().__init__(
            kind=ReaderKind.PROJECTION,
            filename=filename,
            season=season,
            primary_col="Player",
            rank_col='Rank',
            position_col='N/A',
            sheet_name="Sheet 1",
        )
        self.weight = 75

    def get_by_rgx(self, filter_regex: str):
        return super().get_by_rgx(filter_regex)[[
            self.rank_col,
            self.primary_col,
            'Team',
            'Points'
        ]]
