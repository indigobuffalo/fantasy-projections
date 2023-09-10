import pandas as pd

from reader.base import BaseReader


class KKUPFLAdpReader(BaseReader):

    def __init__(self, adp_file: str):
        super().__init__(adp_file)
        self.players_col = 'Player '
        self.adp_col = 'Mock ADP'

    def get_player(self, name: str):
        return self.df.loc[self.df[self.players_col] == name]

    def get_player_rank(self, name: str):
        return self.get_player(name)[self.adp_col][0]

    def get_player_partial_match(self, name: str):
        return self.df.loc[self.df[self.players_col].str.contains(name, na=False, case=False)]

    def get_players(self, players: list[str]):
        player_dfs = list()
        for p in players:
            player_dfs.append(self.get_player_partial_match(p))
        return pd.concat(player_dfs)
