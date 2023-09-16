from collections import defaultdict
from pathlib import Path

import pandas as pd
from unidecode import unidecode

from model.rank import Rank

PROJECTIONS_DIR = Path(__file__).parent.parent / "projections"


class FantasyBaseReader:
    def __init__(self, kind: str, filename, name_col, rank_col, weight=1, ascending=True, sheet_name=0):
        self.kind = kind
        self.ascending = ascending
        self.rank_col = rank_col
        self.name_col = name_col
        self.weight = weight
        self.df = pd.read_excel(PROJECTIONS_DIR / filename, sheet_name=sheet_name, index_col=None)
        self.normalize_player_names()

    def __str__(self):
        return self.kind

    def normalize_player_names(self):
        def normalize(name):
            if isinstance(name, str):
                if name == "Frederik Anderson":
                    name = "Frederik Andersen"
                if name == "Joel Eriksson-Ek":
                    name = "Joel Eriksson Ek"
                if name == "Matthew Boldy":
                    name = "Matt Boldy"
                if name == "Michael Matheson":
                    name = "Mike Matheson"
                if name == "Mitchell Marner":
                    name = "Mitch Marner"
                if name == "Phoenix Copley":
                    name = "Pheonix Copley"
                if name == "Phillipp Grubauer":
                    name = "Philipp Grubauer"
                if name == "Vitek Vanicek":
                    name = "Vitek Vanecek"
                return unidecode(name).title()
            return name
        self.df[self.name_col] = self.df[self.name_col].apply(normalize)

    def print_header(self):
        chars = len(str(self))
        border = '=' * chars
        print(f"{border}\n{self}\n{border}")

    def get_player(self, name: str):
        """
        Get rows of players whose names match the passed regex
        """
        return self.df.loc[self.df[self.name_col].str.contains(name, na=False, case=False)]

    def get_players(self, *players: str):
        """
        Get rows of players whose names match the passed regexes
        """
        player_dataframes = list()
        for p in players:
            player_dataframes.append(self.get_player(p))
        res = pd.concat(player_dataframes)
        return res.round(decimals=1).sort_values(by=[self.rank_col], ascending=self.ascending)

    @staticmethod
    def inc_weight_count(name: str, rankings: dict):
        if rankings[name].get('count'):
            rankings[name]['count'] = rankings[name]['count'] + 1
        else:
            rankings[name]['count'] = 1

    def append_rank(self, name: str, rank: int, rankings: dict):
        if rankings.get(name) and rankings[name].get('ranks'):
            rankings[name]['ranks'].append(Rank(name=name, rank=rank, source=str(self), weight=self.weight))
        else:
            rankings[name] = {'ranks': [Rank(name=name, rank=rank, source=str(self), weight=self.weight)]}

    def record_player_ranks(self, name: str, rankings: dict):
        player_rankings = self.get_player(name)[self.rank_col]
        for rank in player_rankings.values:
            self.append_rank(name, rank, rankings)
            self.inc_weight_count(name, rankings)
