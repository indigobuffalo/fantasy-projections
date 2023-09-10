from pathlib import Path

import pandas as pd

PROJECTIONS_DIR = Path(__file__).parent.parent / "projections"


class FantasyBaseReader:
    def __init__(self, kind: str, filename, players_col, sheet_name=0):
        self.kind = kind
        self.df = pd.read_excel(PROJECTIONS_DIR / filename, sheet_name=sheet_name, index_col=None)
        self.players_col = players_col

    def __str__(self):
        chars = len(self.kind)
        border = '=' * chars
        return f"{border}\n{self.kind}\n{border}"

    def get_player(self, name: str):
        """
        Get rows of players whose names match the passed regex
        """
        return self.df.loc[self.df[self.players_col].str.contains(name, na=False, case=False)]

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
        return res.round(decimals=2)
