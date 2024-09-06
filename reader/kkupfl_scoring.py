import pandas as pd

from reader.base import FantasyBaseReader


class KKUPFLScoringReader(FantasyBaseReader):

    def __init__(self, filename: str, sheet_name: str, ascending=False):
        super().__init__(f"KKUPFL Scoring {sheet_name}", filename, primary_col="Player Name", rank_col='TOTAL / GP', ascending=ascending, sheet_name=sheet_name)
        self.players_col = 'Player Name'
        self.weight = 0

    def filter_by_regex(self, filter_regex: str):
        return super().filter_by_regex(filter_regex)[[
            self.rank_col,
            self.primary_col,
            'Team',
            'Pos',
            'TOTAL',
            'GP',
            'G',
            'A',
            'Pts',
            'SOG',
            'Hits',
            'BS'
        ]]
