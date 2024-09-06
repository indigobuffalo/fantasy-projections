import csv
from pathlib import Path

from pandas import DataFrame

from input.drafted_kkupfl import KKUPFL_DRAFTED
from model.league import League
from reader.base import FantasyBaseReader
from reader.schedule import JeffMaiScheduleReader

OUTPUT_DIR = Path(__file__).parent / "output"


def populate_averaged_rankings(rankings: dict):
    """{<player>: { "ranks": [R1, R2, ...], "count": len(ranks)}}"""
    for player in rankings:
        ranks = [r for r in rankings[player]['ranks']]
        total_weighted_rank = sum([x.rank * x.weight for x in ranks])
        total_weight = sum([x.weight for x in ranks])
        rankings[player]['avg_rk'] = total_weighted_rank / total_weight


def write_avg_ranks_to_csv(league: League, sorted_ranks: list):
    outfile = OUTPUT_DIR / f"{league}_ranks.csv"
    print(f"Writing results for {league} to {outfile}")
    with open(outfile, "w", newline="") as f:
        writer = csv.writer(f)
        for rank_info in sorted_ranks:
            name = rank_info[0]
            avg_rank = round(rank_info[1]['avg_rk'], 2)
            count = rank_info[1]['count']
            ranks = "  |".join(["  " + str(r) for r in rank_info[1]['ranks'] if r.weight > 0])
            writer.writerow([name, avg_rank, count, ranks])


class RankingsController:
    def __init__(self, readers: list[FantasyBaseReader]):
        self.readers = readers

    @staticmethod
    def print_results(results: DataFrame):
        print(f"({len(results)} players)")
        print(results.to_string(index=False))

    def get_rows_matching_regexes(self, reader: FantasyBaseReader, regexes: list[str]):
        return reader.filter_by_regexes(regexes)

    def register_to_averaged_rankings(reader: FantasyBaseReader, results: DataFrame, average_rankings: dict):
        for player_name in results[reader.primary_col]:
            reader.add_to_averaged_rankings(player_name, average_rankings)

    def print_matches_for_reader(self, reader: FantasyBaseReader, results: DataFrame, avg_ranks: dict, name_regexes: list[str]):
        reader.print(results)

    def print_matches_for_all_readers(self, name_regexes: list[str] = None, avg_ranks: dict = None, write: bool = False):
        if name_regexes is None:
            name_regexes = ['.*']
        if avg_ranks is None:
            avg_ranks = dict()
        for reader in self.readers:
            results = self.get_rows_matching_regexes(reader, regexes=name_regexes)
            self.print_matches_for_reader(reader, results, avg_ranks, name_regexes)
