import pandas as pd

from reader.base import FantasyBaseReader


class KKUPFLAdpReader(FantasyBaseReader):

    def __init__(self, adp_file: str):
        super().__init__("KKUPFL ADP", adp_file, name_col='Player ', rank_col='Mock ADP')
        self.adp_col = 'Mock ADP'
        self.weight = 30

    def get_player(self, name: str):
        return super().get_player(name)[[
            'Player ',
            'POS',
            'Mock ADP',
            'Last 5 Mock ADP',
            'Count',
            'Min',
            'Max',
            'Variance',
            'Round'
        ]]
