import pandas as pd

from model.kind import ReaderKind
from reader.base import FantasyBaseReader


class KKUPFLScoringReader(FantasyBaseReader):

    def __init__(self, filename: str, sheet_name: str, ascending=False):
        self.sheet_name = sheet_name
        super().__init__(ReaderKind.HISTORICAL, filename, primary_col="Player Name", rank_col='TOTAL / GP', position_col='Pos', ascending=ascending, sheet_name=sheet_name)
        self.weight = 0

    def __str__(self):
        return f"{self.filename.stem} ({self.sheet_name})"

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
