import pandas as pd

from reader.base import FantasyBaseReader


class SteveLaidlawReader(FantasyBaseReader):

    def __init__(self, adp_file: str, rank_col='Rank', ascending=True):
        super().__init__(f"Steve Laidlaw {rank_col}", adp_file, name_col="Name", rank_col=rank_col, ascending=ascending, sheet_name="Skater Rankings")
        self.players_col = 'NAME'
        self.weight = 15

    def get_player(self, name: str):
        return super().get_player(name)[[
            'Name',
            'Rank',
            'GP',
            'G',
            'A',
            'PPP',
            'SOG',
            'Hits',
            'Points',
        ]]
