import warnings

from controller import ProjectionsController, populate_average_rank, write_avg_ranks_to_csv
from input import players
from reader.dom import DomReader
from reader.ep import EliteProspectsReader
from reader.kkupfl_adp import KKUPFLAdpReader
from reader.kkupfl_scoring import KKUPFLScoringReader
from reader.laidlaw import SteveLaidlawReader

KKUPFL_ADP_FILE = 'KKUPFL_2023_2024_Mock_ADP.xlsx'
KKUPFL_SCORING_FILE = 'KKUPFL_2023_2024_Scoring.xlsx'
DOM_KKUPFL_PROJECTIONS_FILE = 'Dom_2023_2024_KKUPFL.xlsx'
DOM_PA_PROJECTIONS_FILE = 'Dom_2023_2024_Puckin_Around.xlsx'
EP_PROJECTIONS_FILE = 'EP_202324.xlsx'
STEVE_LAIDLAW_PROJECTIONS_FILE = 'Steve_Laidlaw_2023_24.xlsx'


# https://stackoverflow.com/questions/54976991/python-openpyxl-userwarning-unknown-extension-issue
warnings.simplefilter("ignore")


def get_kkupfl_controller():
    kkupfl_scoring_23 = KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202223")
    kkupfl_scoring_22 = KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202122")
    kkupfl_scoring_21 = KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202021")
    dom_rk = DomReader(DOM_KKUPFL_PROJECTIONS_FILE, "kkupfl")
    dom_ppg = DomReader(DOM_KKUPFL_PROJECTIONS_FILE, "kkupfl", rank_col='/GP', ascending=False)
    return ProjectionsController(
        dom_rk,
        dom_ppg,
        kkupfl_scoring_23,
        kkupfl_scoring_22,
        kkupfl_scoring_21,
    )


def get_puckin_around_controller():
    dom_rk = DomReader(DOM_PA_PROJECTIONS_FILE, "puckin around")
    dom_ppg = DomReader(DOM_PA_PROJECTIONS_FILE, "puckin around", rank_col='/GP', ascending=False)
    return ProjectionsController(dom_rk, dom_ppg)


def get_common_controller():
    kkupfl_adp = KKUPFLAdpReader(KKUPFL_ADP_FILE)
    ep = EliteProspectsReader(EP_PROJECTIONS_FILE)
    laidlaw = SteveLaidlawReader(STEVE_LAIDLAW_PROJECTIONS_FILE)
    return ProjectionsController(ep, laidlaw, kkupfl_adp)


if __name__ == '__main__':
    aggregated_ranks = dict()
    common_controller = get_common_controller()
    pa_controller = get_puckin_around_controller()
    # kkupfl_controller = get_kkupfl_controller()
    # kkupfl_controller.compare_players(
        # aggregated_ranks,
        # '.*',
    # )
    common_controller.compare_players(aggregated_ranks, players)
    pa_controller.compare_players(aggregated_ranks, players)
    populate_average_rank(aggregated_ranks)
    sorted_players = sorted(aggregated_ranks.items(), key=lambda item: item[1]['avg_rk'])
    write_avg_ranks_to_csv(sorted_players)
