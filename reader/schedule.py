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

    def filter_primary_row(self, filter_regex: str):
        return super().filter_primary_row(filter_regex)[[
            'team',
            'Grand Total',
        ]]
