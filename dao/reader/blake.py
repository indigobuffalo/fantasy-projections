import pandas as pd

from model.kind import ReaderKind
from dao.reader.base import BaseProjectionsReader


class BlakeRedditReader(BaseProjectionsReader):

    def __init__(self, filename: str, rank_col='Rank', primary_col="Name"):
        super().__init__(ReaderKind.PROJECTION, filename, primary_col=primary_col, rank_col=rank_col, position_col='Pos', sheet_name="Skaters Trimmed")
        self.weight = 75

    def find_by_rgx(self, filter_regex: str):
        return super().find_by_rgx(filter_regex)[[
            self.rank_col,
            self.primary_col,
            'Proj Pos',
            self.position_col,
            'FPTS per GP',
            'PTS',
            'G',
            'A',
            'GP',

            'PPP',
            'SOG',
            'HIT',
            'BLK',
            'S%',
            'ATOI',
        ]]
