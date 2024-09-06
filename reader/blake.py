import pandas as pd

from reader.base import FantasyBaseReader


class BlakeRedditReader(FantasyBaseReader):

    def __init__(self, filename: str, rank_col='FPTS - Total', primary_col="Name"):
        super().__init__(f"Blake", filename, primary_col=primary_col, rank_col=rank_col, sheet_name="Skaters Trimmed", ascending=False)
        self.weight = 75

    def filter_by_regex(self, filter_regex: str):
        return super().filter_by_regex(filter_regex)[[
            self.rank_col,
            self.primary_col,
            'FPTS per GP',
            'GP',
            'G',
            'A',
            'PTS',
            'PPP',
            'SOG',
            'HIT',
            'BLK',
            'S%',
            'ATOI',
        ]]
