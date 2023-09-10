import pandas as pd

from reader.base import FantasyBaseReader


class DomReader(FantasyBaseReader):

    def __init__(self, adp_file: str):
        super().__init__("DOM", adp_file, players_col="NAME", sheet_name="The List")
        self.players_col = 'NAME'

    def get_player(self, name: str):
        return super().get_player(name)[[
            'NAME',
            'POS',
            'RK',
            'AGE',
            'SALARY',
            'FP',
            '/GP',
            'VORP',
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
