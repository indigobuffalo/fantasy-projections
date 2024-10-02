import pandas as pd

from dao.reader.base import BaseProjectionsReader
from model.kind import ReaderKind
from model.season import Season


class KKUPFLScoringReader(BaseProjectionsReader):

    seasons = [
        Season.SEASON_2023_2024, 
        Season.SEASON_2024_2025
    ]

    def __init__(
        self, 
        filename: str, 
        season: Season,
        sheet_name: str, 
        ascending=False
    ):
        self.sheet_name = sheet_name
        super().__init__(
            kind=ReaderKind.HISTORICAL, 
            filename=filename, 
            season=season,
            primary_col="Player Name", 
            rank_col='TOTAL / GP', 
            position_col='Pos', 
            ascending=ascending, 
            sheet_name=sheet_name
        )
        self.weight = 0

    def __str__(self):
        return f"{self.season}__{self.filename.stem}__{self.rank_col}  - {self.sheet_name}"

    def query_primary_col(self, query: str, limit: int = -1):
        return super().query_primary_col(query, limit)[[
            self.rank_col,
            self.primary_col,
            self.position_col,
            'Team',
            'TOTAL',
            'GP',
            'G',
            'A',
            'Pts',
            'SOG',
            'Hits',
            'BS'
        ]]
