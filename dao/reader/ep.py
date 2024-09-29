import pandas as pd

from dao.reader.base import BaseProjectionsReader
from model.kind import ReaderKind


class EliteProspectsReader(BaseProjectionsReader):

    def __init__(self, filename: str, rank_col='Rank'):
        super().__init__(
            ReaderKind.PROJECTION,
            filename,
            primary_col="Name",
            rank_col=rank_col,
            position_col='Pos',
            team_col="Team"
        )
        self.weight = 75

    def find_by_rgx(self, filter_regex: str):
        return super().find_by_rgx(filter_regex)[[
            self.rank_col,
            self.primary_col,
            self.position_col,
            'Team',
            'Points',
            'Games',
            'Goals',
            'Assists'
        ]]
