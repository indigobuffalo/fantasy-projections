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

    @staticmethod
    def from_yahoo_week(yahoo_week: int) -> int:
        """Convert a yahoo week to a week on the Jeff Mai schedule"""
        return yahoo_week + 1

    def filter_primary_row(self, filter_regex: str):
        return super().filter_primary_row(filter_regex)[[
            self.rank_col,
            self.primary_col
        ]]

    def filter_weeks(self, filter_regexes: list[str], start: int, end: int):
        dataframes = list()
        cols = [self.primary_col]
        start, end = self.from_yahoo_week(start), self.from_yahoo_week(end)
        weeks = [w for w in range(start, end + 1)]
        cols.extend(weeks)
        cols.append(self.rank_col)
        for fr in filter_regexes:
            df = self.df.loc[self.df[self.primary_col].str.contains(fr, na=False, case=False)][cols]
            dataframes.append(df)
        res = pd.concat(dataframes)
        for w in weeks:
            res[w] = res[w].astype(int)
        res[self.rank_col] = res[self.rank_col].astype(int)
        return res.sort_values(by=[self.rank_col], ascending=self.ascending)
