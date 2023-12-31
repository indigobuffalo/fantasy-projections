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
        self.players_col = 'Player'
        self.weight = 75

    def filter_primary_row(self, filter_regex: str):
        return super().filter_primary_row(filter_regex)[[
            self.rank_col,
            self.primary_col,
            'Team',
            'Points'
        ]]
