import pandas as pd

from dao.reader.base import BaseProjectionsReader
from model.kind import ReaderKind


class SteveLaidlawReader(BaseProjectionsReader):

    def __init__(self, filename: str, rank_col='Rank'):
        super().__init__(ReaderKind.PROJECTION, filename, primary_col="Name", rank_col=rank_col, position_col='N/A', sheet_name="Skaters Rankings")
        self.weight = 75

    def find_by_rgx(self, filter_regex: str):
        return super().find_by_rgx(filter_regex)[[
            self.rank_col,
            self.primary_col,
            'GP',
            'G',
            'A',
            'P',
            'PPP',
            'SOG',
            'Hits',
            'Blks'
        ]]
