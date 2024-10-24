import pandas as pd

from model.kind import ReaderKind
from dao.base import FantasyBaseDao


class DomDao(FantasyBaseDao):

    def __init__(self, filename: str, rank_col='RK', ascending=True):
        super().__init__(
            ReaderKind.PROJECTION,
            filename,
            primary_col="NAME",
            rank_col=rank_col,
            position_col='POS',
            team_col="TEAM",
            ascending=ascending,
            sheet_name="The List"
        )
        self.weight = 700 if self.rank_col == 'RK' else 0  # don't weigh /GP rank

    def __str__(self):
        return f"{self.filename.stem} ({self.rank_col}))"

    def find_by_rgx(self, filter_regex: str):
        return super().find_by_rgx(filter_regex)[[
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
