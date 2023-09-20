import csv
from pathlib import Path

from pandas import DataFrame

from reader.base import FantasyBaseReader
from reader.ep import EliteProspectsReader
from reader.kkupfl_adp import KKUPFLAdpReader
from reader.laidlaw import SteveLaidlawReader

OUTPUT_DIR = Path(__file__).parent / "output"
KKUPFL_ADP_FILE = 'KKUPFL_2023_2024_Mock_ADP.xlsx'
EP_PROJECTIONS_FILE = 'EP_202324.xlsx'
STEVE_LAIDLAW_PROJECTIONS_FILE = 'Steve_Laidlaw_2023_24.xlsx'


def populate_average_rank(rankings: dict):
    """{<player>: { "ranks": [R1, R2, ...], "count": len(ranks)}}"""
    for player in rankings:
        ranks = [r for r in rankings[player]['ranks']]
        total_weighted_rank = sum([x.rank * x.weight for x in ranks])
        total_weight = sum([x.weight for x in ranks])
        rankings[player]['avg_rk'] = total_weighted_rank / total_weight


def write_avg_ranks_to_csv(sorted_ranks: list):
    with open(OUTPUT_DIR / "average_ranks.csv", "w", newline="") as f:
        writer = csv.writer(f)
        for rank_info in sorted_ranks:
            name = rank_info[0]
            avg_rank = round(rank_info[1]['avg_rk'], 2)
            count = rank_info[1]['count']
            ranks = "  |".join(["  " + str(r) for r in rank_info[1]['ranks'] if r.weight > 0])
            writer.writerow([name, avg_rank, count, ranks])


class ProjectionsController:
    def __init__(self, *readers: FantasyBaseReader):

        kkupfl_adp = KKUPFLAdpReader(KKUPFL_ADP_FILE)
        ep = EliteProspectsReader(EP_PROJECTIONS_FILE)
        laidlaw = SteveLaidlawReader(STEVE_LAIDLAW_PROJECTIONS_FILE)
        base_readers = [kkupfl_adp, ep, laidlaw]
        self.readers = base_readers + list(readers)

    @staticmethod
    def print_results(results: DataFrame):
        print(f"({len(results)} players)")
        print(results.to_string(index=False))

    def run_reader(self, reader: FantasyBaseReader, avg_ranks: dict, players: list[str]):
        reader.print_header()
        results = reader.get_players(players)
        self.print_results(results)
        for p in results[reader.name_col]:
            reader.record_player_ranks(p, avg_ranks)
        return results

    def compare_players(self, avg_ranks: dict, players: list[str]):
        for reader in self.readers:
            self.run_reader(reader, avg_ranks, players)
