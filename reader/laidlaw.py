import pandas as pd

from reader.base import FantasyBaseReader


class SteveLaidlawReader(FantasyBaseReader):

    def __init__(self, filename: str, rank_col='Rank'):
        super().__init__(f"Steve Laidlaw {rank_col}", filename, primary_col="Name", rank_col=rank_col, sheet_name="Skaters Rankings")
        self.weight = 75

    def filter_by_regex(self, filter_regex: str):
        return super().filter_by_regex(filter_regex)[[
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
