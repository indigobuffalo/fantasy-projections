import csv
import warnings
from pathlib import Path
from pprint import pprint

from controller import ProjectionsController
from reader.dom import DomReader
from reader.ep import EliteProspectsReader
from reader.kkupfl_adp import KKUPFLAdpReader
from reader.kkupfl_scoring import KKUPFLScoringReader

KKUPFL_ADP_FILE = 'KKUPFL_2023_2024_Mock_ADP.xlsx'
KKUPFL_SCORING_FILE = 'KKUPFL_2023_2024_Scoring.xlsx'
DOM_KKUPFL_PROJECTIONS_FILE = 'Dom_2023_2024_KKUPFL.xlsx'
DOM_PA_PROJECTIONS_FILE = 'Dom_2023_2024_Puckin_Around.xlsx'
EP_PROJECTIONS_FILE = 'EP_202324.xlsx'

OUTPUT_DIR = Path(__file__).parent / "output"


# https://stackoverflow.com/questions/54976991/python-openpyxl-userwarning-unknown-extension-issue
warnings.simplefilter("ignore")


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


if __name__ == '__main__':
    aggregated_ranks = dict()

    # kkupfl
    kkupfl_adp = KKUPFLAdpReader(KKUPFL_ADP_FILE)
    kkupfl_scoring_23 = KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202223")
    kkupfl_scoring_22 = KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202122")
    kkupfl_scoring_21 = KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202021")

    dom_kkupfl_rk = DomReader(DOM_KKUPFL_PROJECTIONS_FILE, "kkupfl")
    dom_kkupfl_ppg = DomReader(DOM_KKUPFL_PROJECTIONS_FILE, "kkupfl", rank_col='/GP', ascending=False)

    # puckin around
    # dom_pa_rk = DomReader(DOM_PA_PROJECTIONS_FILE, "puckin around")
    # dom_pa_ppg = DomReader(DOM_PA_PROJECTIONS_FILE, "puckin around", rank_col='/GP', ascending=False)

    # general
    ep = EliteProspectsReader(EP_PROJECTIONS_FILE)

    import ipdb; ipdb.set_trace()

    pc = ProjectionsController(
        dom_kkupfl_rk,
        # dom_pa_rk,
        kkupfl_adp,
        ep,
        dom_kkupfl_ppg,
        # dom_pa_ppg,
        kkupfl_scoring_23,
        kkupfl_scoring_22,
        kkupfl_scoring_21,
    )
    pc.record_comparisons(
        aggregated_ranks,
        '^J.* Mark',
        '^Se.* Bob',
        '^T.* Chabo',
        '^D.* Toew',
        '^Nico.* Hisc',
        '^Tyler.* Toff',
    )

    populate_average_rank(aggregated_ranks)
    sorted_players = sorted(aggregated_ranks.items(), key=lambda item: item[1]['avg_rk'])
    write_avg_ranks_to_csv(sorted_players)

