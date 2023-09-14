from collections import defaultdict

from reader.base import FantasyBaseReader


class ProjectionsController:
    def __init__(self, *readers: FantasyBaseReader):
        self.readers = readers

    def compare(self, avg_ranks: dict, *players: str):
        for r in self.readers:
            r.print_fmt()
            res = r.get_players(*players)
            print(f"({len(res)} players)")
            print(res.to_string(index=False))
            for p in res[r.name_col]:
                r.populate_player_ranks(p, avg_ranks)
