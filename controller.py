from collections import defaultdict

from pandas import DataFrame

from reader.base import FantasyBaseReader


class ProjectionsController:
    def __init__(self, *readers: FantasyBaseReader):
        self.readers = readers

    @staticmethod
    def print_results(results: DataFrame):
        print(f"({len(results)} players)")
        print(results.to_string(index=False))

    def record_comparisons(self, avg_ranks: dict, *players: str):
        for r in self.readers:
            r.print_header()
            res = r.get_players(*players)
            self.print_results(res)
            for p in res[r.name_col]:
                r.record_player_ranks(p, avg_ranks)
