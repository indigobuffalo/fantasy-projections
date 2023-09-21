from collections import defaultdict
from pathlib import Path

import pandas as pd
from unidecode import unidecode

from model.rank import Rank

PROJECTIONS_DIR = Path(__file__).parent.parent / "rankings"

name_correction_map = {
    "ALEXANDER OVECHKIN": "Alex Ovechkin",
    "FREDERIK ANDERSON": "Frederik Andersen",
    "JOEL ERIKSSON-EK": "Joel Eriksson Ek",
    "JT MILLER": "J.T. Miller",
    "MATTHEW BOLDY": "Matt Boldy",
    "MICHAEL MATHESON": "Mike Matheson",
    "MITCHELL MARNER": "Mitch Marner",
    "PHOENIX COPLEY": "Pheonix Copley",
    "PILLIPP GRUBAUER": "Philipp Grubauer",
    "VITEK VANICEK": "Vitek Vanecek"
}


class FantasyBaseReader:
    def __init__(self, kind: str, filename, name_col, rank_col, team_col=None, weight=1, ascending=True, sheet_name=0):
        self.kind = kind
        self.ascending = ascending
        self.rank_col = rank_col
        self.name_col = name_col
        self.team_col = team_col
        self.weight = weight
        self.df = pd.read_excel(PROJECTIONS_DIR / filename, sheet_name=sheet_name, index_col=None)
        self.normalize_player_names()

    def __str__(self):
        return self.kind

    @staticmethod
    def normalize_spelling(name):
        upper = name.upper()
        return name_correction_map[upper] if upper in name_correction_map else name

    @staticmethod
    def normalize_accents(name):
        return unidecode(name)

    @staticmethod
    def normalize_capitalization(name):
        return name.title()

    def normalize_player_names(self):
        def normalize(name):
            if not isinstance(name, str):
                return name
            name = self.normalize_spelling(name)
            name = self.normalize_accents(name)
            name = self.normalize_capitalization(name)
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

    def get_players(self, players: list[str]):
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

    def record_player_ranks(self, name: str, rankings: dict, teams: set):
        player = self.get_player(name)
        if self.team_col:
            teams.add(player[self.team_col].values[0])
        player_rankings = player[self.rank_col]
        for rank in player_rankings.values:
            self.append_rank(name, rank, rankings)
            self.inc_weight_count(name, rankings)
