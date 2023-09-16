import pandas as pd

from reader.base import FantasyBaseReader


class EliteProspectsReader(FantasyBaseReader):

    def __init__(self, adp_file: str, rank_col='Rank', ascending=True):
        super().__init__(f"Elite Prospects {rank_col}", adp_file, name_col="Player",
                         rank_col=rank_col, ascending=ascending)
        self.players_col = 'NAME'
        self.weight = 10

    def get_player(self, name: str):
        return super().get_player(name)[[
            'Rank',
            'Player',
            'Pos',
            'Team',
            'GP',
            'G',
            'A',
            'P',
            'GP.1',
            'W',
        ]]
