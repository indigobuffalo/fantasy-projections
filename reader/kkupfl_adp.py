import pandas as pd

from reader.base import FantasyBaseReader


class KKUPFLAdpReader(FantasyBaseReader):

    def __init__(self, filename: str):
        super().__init__("KKUPFL ADP", filename, primary_col='Player ', rank_col='Mock ADP')
        self.adp_col = 'Mock ADP'
        self.weight = 30

    def filter_primary_row(self, filter_regex: str):
        return super().filter_primary_row(filter_regex)[[
            self.rank_col,
            self.primary_col,
            'POS',
            'Last 5 Mock ADP',
            'Count',
            'Min',
            'Max',
            'Variance',
            'Round'
        ]]
