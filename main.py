import warnings
from collections import defaultdict

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


# https://stackoverflow.com/questions/54976991/python-openpyxl-userwarning-unknown-extension-issue
warnings.simplefilter("ignore")

if __name__ == '__main__':
    avg_ranks = defaultdict(list)

    # kkupfl
    kkupfl_adp = KKUPFLAdpReader(KKUPFL_ADP_FILE)
    kkupfl_scoring_23 = KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202223")
    kkupfl_scoring_22 = KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202122")
    kkupfl_scoring_21 = KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202021")

    dom_kkupfl_rk = DomReader(DOM_KKUPFL_PROJECTIONS_FILE, "kkupfl")
    dom_kkupfl_ppg = DomReader(DOM_KKUPFL_PROJECTIONS_FILE, "kkupfl", rank_col='/GP', ascending=False)

    # puckin around
    dom_pa_rk = DomReader(DOM_PA_PROJECTIONS_FILE, "puckin around")
    dom_pa_ppg = DomReader(DOM_PA_PROJECTIONS_FILE, "puckin around", rank_col='/GP', ascending=False)

    # general
    ep = EliteProspectsReader(EP_PROJECTIONS_FILE)

    pc = ProjectionsController(
        dom_kkupfl_rk,
        dom_pa_rk,
        ep,
        kkupfl_adp,
        dom_kkupfl_ppg,
        dom_pa_ppg,
        kkupfl_scoring_23,
        kkupfl_scoring_22,
        kkupfl_scoring_21,
    )
    pc.compare(
        avg_ranks,
        '^B.* Tkach',
        '^J.* Miller',
    )
