import pandas as pd

from reader.base import FantasyBaseReader


class EliteProspectsReader(FantasyBaseReader):

    def __init__(self, filename: str, rank_col='Points'):
        super().__init__(
            f"Elite Prospects {rank_col}",
            filename,
            primary_col="Name",
            rank_col=rank_col,
            team_col="Team",
        )
        self.weight = 75

    def filter_by_regex(self, filter_regex: str):
        return super().filter_by_regex(filter_regex)[[
            self.rank_col,
            self.primary_col,
            'Pos',
            'Team',
            'Games',
            'Goals',
            'Assists'
        ]]
