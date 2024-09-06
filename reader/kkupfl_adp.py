import pandas as pd

from reader.base import FantasyBaseReader


class KKUPFLAdpReader(FantasyBaseReader):

    def __init__(self, filename: str):
        super().__init__("KKUPFL ADP", filename, primary_col='Player', rank_col='Full MOCK ADP ')
        self.adp_col = 'Mock ADP'
        self.weight = 75

    def filter_by_regex(self, filter_regex: str):
        return super().filter_by_regex(filter_regex)[[
            self.rank_col,
            self.primary_col,
            'POS',
            'POS Rank',
            'Count',
            'Min',
            'Max',
            'Variance',
        ]]
