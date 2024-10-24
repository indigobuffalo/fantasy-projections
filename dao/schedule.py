from datetime import datetime

import numpy
import pandas as pd
from pandas import DataFrame

from model.kind import ReaderKind
from dao.base import FantasyBaseDao


class JeffMaiScheduleDao(FantasyBaseDao):
    """
    Reader for schedule created by Jeff Mai:
      https://docs.google.com/spreadsheets/d/1kze7d9SfT7xEQQLHCkgPIpyNqxhnxfSpSw_H2p_vdmw/edit#gid=1251157188
      https://www.reddit.com/r/fantasyhockey/comments/15xkdg5/202324_nhl_schedule/

    Playoffs:
      YAHOO:    Week 23, 24 and 25
      JEFF MAI: Week 24, 25 and 26
    """

    def __init__(
            self,
            filename: str,
            rank_col: str = 'Grand Total',
            ascending: bool = False,
            sheet_name: str = "Off night games per week"
    ):
        super().__init__(
            ReaderKind.SCHEDULE,
            filename,
            primary_col="team",
            rank_col=rank_col,
            sheet_name=sheet_name,
            ascending=ascending,
            header=1
        )
        self.rank_col = rank_col
        self.playoff_weeks = {24, 25, 26}

    @staticmethod
    def from_yahoo_week(yahoo_week: int) -> int:
        """Convert a yahoo week to a week on the Jeff Mai schedule"""
        return yahoo_week + 1

    @staticmethod
    def to_yahoo_week(jeff_mai_week: int) -> int:
        """Convert a Jeff Mai week to a Yahoo week"""
        return jeff_mai_week - 1

    @staticmethod
    def floats_to_ints(df: DataFrame, columns: list):
        for c in columns:
            if isinstance(df[c].values[0], numpy.float64):
                df[c] = df[c].astype(int)

    @staticmethod
    def jeff_mai_weeks_to_yahoo_weeks(df: DataFrame, columns: list):
        for c in columns:
            if isinstance(c, int):
                # TODO: fix issue with footer column throwing this off
                df.rename(columns={c: c-1}, inplace=True)

    def find_by_rgx(self, filter_regex: str):
        cols = [self.rank_col, self.primary_col] + list(self.playoff_weeks)
        res = super().find_by_rgx(filter_regex)[cols]
        self.floats_to_ints(res, cols)
        self.jeff_mai_weeks_to_yahoo_weeks(res, cols)
        return res
