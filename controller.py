import csv
from pathlib import Path

from pandas import DataFrame

from config.config import FantasyConfig
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
    outfile = OUTPUT_DIR / FantasyConfig.season / f"{league}_ranks.csv"
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

    def get_rows_matching_regexes(self, reader: FantasyBaseReader, regexes: list[str]) -> DataFrame:
        return reader.filter_by_regexes(regexes)

    @staticmethod
    def register_to_averaged_rankings(reader: FantasyBaseReader, results: DataFrame, average_rankings: dict):
        for player_name in results[reader.primary_col]:
            reader.add_to_averaged_rankings(player_name, average_rankings)

    def get_matches_for_all_readers(self, regexes) -> dict[FantasyBaseReader, DataFrame]:
        '''
        Searches all readers for rows matching the passed in regexes.

        Returns a dictionary which maps each reader to its corresponding result set.
        '''
        if regexes is None:
            regexes = ['.*']
        reader_results = dict()
        for reader in self.readers:
            reader_results[reader] = self.get_rows_matching_regexes(reader, regexes=regexes)
        return reader_results

    def print_matches_for_all_readers(self, reader_results_map: dict[FantasyBaseReader, DataFrame]) -> None:
        for reader, results in reader_results_map.items():
            reader.print(results)
