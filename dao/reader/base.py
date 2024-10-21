from abc import ABCMeta, abstractmethod
from pathlib import Path

import pandas as pd
from pandas import DataFrame
from model.season import Season
from unidecode import unidecode

from exceptions import UnrecognizedPlayerError
from model.rank import Rank
from config.config import FantasyConfig

PROJECTIONS_DIR = Path(__file__).parent.parent.parent / "data" / "projections"

class BaseProjectionsReader(metaclass=ABCMeta):
    def __init__(
        self, 
        kind: str, 
        filename: str, 
        season: Season,
        primary_col, 
        rank_col, 
        position_col,
        team_col=None,
        weight=1, 
        ascending=True, 
        sheet_name=0, 
        header=0
    ):
        self.kind = kind
        self.season = season
        self.ascending = ascending
        self.rank_col = rank_col
        self.primary_col = primary_col
        self.position_col = position_col
        self.team_col = team_col
        self.weight = weight
        self.filename = PROJECTIONS_DIR / self.season.value / filename
        self.df = pd.read_excel(self.filename, sheet_name=sheet_name, index_col=None, header=header)
        self.normalize()

    def __str__(self):
        return f"{self.season}__{self.filename.stem}__{self.rank_col.strip().replace(" ","-")}"

    @property
    @abstractmethod
    def seasons(self):
        '''The seasons supported by the reader'''
        pass

    @staticmethod
    def normalize_spelling(name):
        upper = name.upper()
        return FantasyConfig.normalized_player_names[upper] if upper in FantasyConfig.normalized_player_names else name

    @staticmethod
    def normalize_accents(name):
        return unidecode(name)

    @staticmethod
    def normalize_capitalization(name):
        return name.title()

    def is_team_reader(self):
        return self.primary_col == "team"

    @staticmethod
    def normalize_team_names(name):
        if not isinstance(name, str):
            return name
        return name.upper()

    def normalize_player_names(self, name):
        if not isinstance(name, str):
            return name
        name = self.normalize_spelling(name)
        name = self.normalize_accents(name)
        name = self.normalize_capitalization(name)
        return name

    def normalize(self):
        if self.is_team_reader():
            self.df[self.primary_col] = self.df[self.primary_col].apply(self.normalize_team_names)
        else:
            self.df[self.primary_col] = self.df[self.primary_col].apply(self.normalize_player_names)

    def filter_by_rgx():
        pass

    def query_primary_col(self, query: str, limit: int = -1) -> DataFrame:
        """Get rows with primary column values that match incl_rgx and do not match excl_rgx.

        Args:
            query (str): A regex to query the primary_column with.
            limit (int): Number of records to return.

        Returns:
            DataFrame: The matching row(s) from the source dataframe.
        """
        matches = self.df.loc[
            self.df[self.primary_col].str.contains(query, na=False, case=False)
        ]
        if limit > 0:
            return matches.head(limit)
        return matches


    def find_by_rgxs(self, filter_regexes: list[str], ) -> DataFrame:
        """Get rows with primary column values that satisfy the passed regex filters

        Args:
            filter_regexes (list[str]): List of regexes to filter upon.

        Returns:
            DataFrame: Matching results, sorted by rank.
        """
        dataframes = list()
        for r in filter_regexes:
            dataframes.append(self.query_primary_col(r))
        res = pd.concat(dataframes)
        return res.round(decimals=1).sort_values(by=[self.rank_col], ascending=self.ascending)

    @staticmethod
    def inc_weight_count(name: str, rankings: dict):
        if rankings[name].get('count'):
            rankings[name]['count'] = rankings[name]['count'] + 1
        else:
            rankings[name]['count'] = 1

    def append_rank(self, name: str, rank: int, rankings: dict):
        if name in rankings:
            rankings[name]['ranks'].append(Rank(name=name, rank=rank, source=str(self), weight=self.weight))
        else:
            rankings[name] = {'ranks': [Rank(name=name, rank=rank, source=str(self), weight=self.weight)]}

    def add_to_averaged_rankings(self, name: str, rankings: dict):
        player_df = self.query_primary_col(name)

        player_rankings = player_df[self.rank_col]
        if len(player_rankings.values) == 0:
            raise UnrecognizedPlayerError(name, self.filename)
        rank = player_rankings.values[0]

        self.append_rank(name, rank, rankings)
        self.inc_weight_count(name, rankings)