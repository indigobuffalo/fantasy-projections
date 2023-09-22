from datetime import datetime

import pandas as pd

from reader.base import FantasyBaseReader


class JeffMaiScheduleReader(FantasyBaseReader):

    # KKUPFL
    # Playoffs end Sunday, Apr 7
    # YAHOO:    Week 23, 24 and 25
    # JEFF MAI: Week 24, 25 and 26

    def __init__(
            self,
            filename: str,
            rank_col: str = 'Grand Total',
            start: int = 0,
            end: int = 0,
            ascending: bool = False,
            sheet_name: str = "Off night games per week"
    ):
        super().__init__(
            f"Jeff Mai Schedule ({rank_col})",
            filename,
            primary_col="team",
            rank_col=rank_col,
            sheet_name=sheet_name,
            ascending=ascending,
            header=1
        )
        self.rank_col = rank_col
        self.playoff_weeks = {24, 25, 26}

    def filter_primary_row(self, filter_regex: str):
        return super().filter_primary_row(filter_regex)[[
            self.rank_col,
            self.primary_col
        ]]
