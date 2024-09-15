import pandas as pd

from model.kind import ReaderKind
from dao.base import FantasyBaseDao


class KKUPFLAdpDao(FantasyBaseDao):

    def __init__(self, filename: str):
        super().__init__(ReaderKind.PROJECTION, filename, primary_col='Player', rank_col='Full MOCK ADP ', position_col='POS')
        self.weight = 75

    def find_by_rgx(self, filter_regex: str):
        return super().find_by_rgx(filter_regex)[[
            self.rank_col,
            self.primary_col,
            self.position_col,
            'POS Rank',
            'Count',
            'Min',
            'Max',
            'Variance',
        ]]
