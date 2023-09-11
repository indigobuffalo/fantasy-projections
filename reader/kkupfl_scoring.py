import pandas as pd

from reader.base import FantasyBaseReader


class KKUPFLScoringReader(FantasyBaseReader):

    def __init__(self, adp_file: str, sheet_name: str, ascending=False):
        super().__init__(f"KKUPFL Scoring {sheet_name}", adp_file, players_col="NAME", rank_col='TOTAL / GP', ascending=ascending, sheet_name=sheet_name)
        self.players_col = 'Player Name'

    def get_player(self, name: str):
        return super().get_player(name)[[
            'Total Rank',
            'Player Name',
            'Pos',
            'TOTAL',
            'TOTAL / GP',
        ]]
