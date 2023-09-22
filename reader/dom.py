import pandas as pd

from reader.base import FantasyBaseReader


class DomReader(FantasyBaseReader):

    def __init__(self, filename: str, league: str, rank_col='RK', ascending=True):
        super().__init__(
            f"DOM {rank_col} ({league.upper()})",
            filename,
            primary_col="NAME",
            rank_col=rank_col,
            team_col="TEAM",
            ascending=ascending,
            sheet_name="The List"
        )
        self.players_col = 'NAME'
        self.weight = 700 if self.rank_col == 'RK' else 0  # don't weigh /GP rank

    def filter_primary_row(self, filter_regex: str):
        return super().filter_primary_row(filter_regex)[[
            self.rank_col,
            self.primary_col,
            'AGE',
            'TEAM',
            'POS',
            'FP',
            'GP',
            'G',
            'A',
            'PTS',
            'SOG',
            'BLK',
            'HIT',
            'GP.1',
            'W',
            'SV',
            'GA'
        ]]
