import pandas as pd

from reader.base import FantasyBaseReader


class DomReader(FantasyBaseReader):

    def __init__(self, adp_file: str, league: str, rank_col='RK', ascending=True):
        super().__init__(f"DOM {rank_col} ({league.upper()})", adp_file, name_col="NAME", rank_col=rank_col, ascending=ascending, sheet_name="The List")
        self.players_col = 'NAME'
        self.weight = 65 if self.rank_col == 'RK' else 0  # don't weigh /GP rank

    def get_player(self, name: str):
        return super().get_player(name)[[
            'NAME',
            'POS',
            'RK',
            'FP',
            '/GP',
            'AGE',
            'GP',
            'G',
            'A',
            'PTS',
            'SOG',
            'BLK',
            'HIT',
            'GP.1',
            'W',
            'SV',
            'GA'
        ]]
