import pandas as pd

from reader.base import FantasyBaseReader


class SteveLaidlawReader(FantasyBaseReader):

    def __init__(self, filename: str, rank_col='Rank'):
        super().__init__(f"Steve Laidlaw {rank_col}", filename, primary_col="Name", rank_col=rank_col, sheet_name="Skater Rankings")
        self.players_col = 'NAME'
        self.weight = 15

    def filter_primary_row(self, filter_regex: str):
        return super().filter_primary_row(filter_regex)[[
            self.rank_col,
            self.primary_col,
            'GP',
            'G',
            'A',
            'PPP',
            'SOG',
            'Hits',
            'Points',
        ]]
