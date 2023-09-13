import pandas as pd

from reader.base import FantasyBaseReader


class KKUPFLScoringReader(FantasyBaseReader):

    def __init__(self, adp_file: str, sheet_name: str, ascending=False):
        super().__init__(f"KKUPFL Scoring {sheet_name}", adp_file, name_col="Player Name", rank_col='TOTAL / GP', ascending=ascending, sheet_name=sheet_name)
        self.players_col = 'Player Name'
        self.weight = 0

    def get_player(self, name: str):
        return super().get_player(name)[[
            'Total Rank',
            'Player Name',
            'Team',
            'Pos',
            'TOTAL',
            'TOTAL / GP',
        ]]
