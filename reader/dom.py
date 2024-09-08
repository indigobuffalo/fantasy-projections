import pandas as pd

from reader.base import FantasyBaseReader


class DomReader(FantasyBaseReader):

    def __init__(self, filename: str, rank_col='RK', ascending=True):
        super().__init__(
            f"DOM ({rank_col})",
            filename,
            primary_col="NAME",
            rank_col=rank_col,
            team_col="TEAM",
            ascending=ascending,
            sheet_name="The List"
        )
        self.weight = 700 if self.rank_col == 'RK' else 0  # don't weigh /GP rank

    def filter_by_regex(self, filter_regex: str):
        return super().filter_by_regex(filter_regex)[[
            self.rank_col,
            self.primary_col,
            'AGE',
            'TEAM',
            'POS',
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
