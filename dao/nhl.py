import pandas as pd

from model.kind import ReaderKind
from dao.base import FantasyBaseDao


class NHLDao(FantasyBaseDao):
    """Projections from nhl.com"""

    def __init__(self, filename: str):
        super().__init__(
            ReaderKind.PROJECTION,
            filename,
            primary_col="Player",
            rank_col='Rank',
            sheet_name="Sheet 1"
        )
        self.weight = 75

    def find_by_rgx(self, filter_regex: str):
        return super().find_by_rgx(filter_regex)[[
            self.rank_col,
            self.primary_col,
            'Team',
            'Points'
        ]]
