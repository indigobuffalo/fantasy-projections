import pandas as pd

from reader.base import FantasyBaseReader


class KKUPFLScoringReader(FantasyBaseReader):

    def __init__(self, filename: str, sheet_name: str, ascending=False):
        super().__init__(f"KKUPFL Scoring {sheet_name}", filename, primary_col="Player Name", rank_col='TOTAL / GP', position_col='Pos', ascending=ascending, sheet_name=sheet_name)
        self.weight = 0

    def find_by_rgx(self, filter_regex: str):
        return super().find_by_rgx(filter_regex)[[
            self.rank_col,
            self.primary_col,
            self.position_col,
            'Team',
            'TOTAL',
            'GP',
            'G',
            'A',
            'Pts',
            'SOG',
            'Hits',
            'BS'
        ]]
