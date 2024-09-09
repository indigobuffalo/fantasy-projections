import pandas as pd

from reader.base import FantasyBaseReader


class NHLReader(FantasyBaseReader):
    """Projections from nhl.com"""

    def __init__(self, filename: str):
        super().__init__(
            f"NHL.com (Points)",
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
