import pandas as pd

from reader.base import FantasyBaseReader


class DomReader(FantasyBaseReader):

    def __init__(self, adp_file: str, rank_col='RK', ascending=True):
        super().__init__(f"DOM {rank_col}", adp_file, players_col="NAME", rank_col=rank_col, ascending=ascending, sheet_name="The List")
        self.players_col = 'NAME'

    def get_player(self, name: str):
        return super().get_player(name)[[
            'NAME',
            'POS',
            'RK',
            'FP',
            '/GP',
            'VORP',
            'AGE',
            'SALARY',
            'GP',
            'TOI',
            'G',
            'A',
            'PTS',
            'PPP',
            'SOG',
            'BLK',
            'HIT'
        ]]
