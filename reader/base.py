from collections import defaultdict
from pathlib import Path

import pandas as pd

from model.rank import Rank

PROJECTIONS_DIR = Path(__file__).parent.parent / "projections"


class FantasyBaseReader:
    def __init__(self, kind: str, filename, name_col, rank_col, weight=1, ascending=True, sheet_name=0):
        self.kind = kind
        self.rank_col = rank_col
        self.ascending = ascending
        self.df = pd.read_excel(PROJECTIONS_DIR / filename, sheet_name=sheet_name, index_col=None)
        self.name_col = name_col
        self.weight = weight

    def __str__(self):
        return self.kind

    def print_fmt(self):
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
        if len(players) == 0:
            res = self.get_player(players[0])
        else:
            player_dfs = list()
            for p in players:
                player_dfs.append(self.get_player(p))
            res = pd.concat(player_dfs)
        return res.round(decimals=1).sort_values(by=[self.rank_col], ascending=self.ascending)

    def populate_player_ranks(self, name: str, rankings: defaultdict[list]):
        player_rankings = self.get_player(name)[[self.name_col, self.rank_col]]
        for name_and_rank in player_rankings.values:
            p_name, p_rank = name_and_rank[0], name_and_rank[1]
            rankings[p_name].append(Rank(name=p_name, rank=p_rank, source=str(self), weight=self.weight))
