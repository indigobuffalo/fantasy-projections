import pandas as pd

from reader.base import FantasyBaseReader


class JeffMaiScheduleReader(FantasyBaseReader):

    def __init__(self, filename: str, rank_col='Grand Total', ascending=False, sheet_name="Off night games per week"):
        super().__init__(
            f"Jeff Mai Schedule {rank_col}",
            filename,
            primary_col="team",
            rank_col=rank_col,
            sheet_name=sheet_name,
            ascending=ascending,
            header=1
        )

    def get_team(self, name: str):
        return super().filter_primary_row(name)[[
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
