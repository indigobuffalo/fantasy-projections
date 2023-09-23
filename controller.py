import csv
from pathlib import Path

from pandas import DataFrame

from input.kkupfl import KKUPFL_DRAFTED
from model.league import League
from reader.base import FantasyBaseReader
from reader.schedule import JeffMaiScheduleReader

OUTPUT_DIR = Path(__file__).parent / "output"


def populate_average_rank(rankings: dict):
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

    def run_reader(self, reader: FantasyBaseReader, avg_ranks: dict, teams: set, players: list[str], write=False):
        if isinstance(reader, JeffMaiScheduleReader) and not write:
            results = reader.filter_primary_rows(list(teams))
        else:
            results = reader.filter_primary_rows(players)
            for p in results[reader.primary_col]:
                reader.record_player_ranks(p, avg_ranks, teams)
        if not write:
            reader.print_header()
            self.print_results(results)

    def compare_players(self, avg_ranks: dict, teams: set, players: list[str], write=False):
        for reader in self.readers:
            self.run_reader(reader, avg_ranks, teams, players, write=write)
