import warnings
from collections import defaultdict

from controller import ProjectionsController
from reader.dom import DomReader
from reader.ep import EliteProspectsReader
from reader.kkupfl_adp import KKUPFLAdpReader
from reader.kkupfl_scoring import KKUPFLScoringReader

KKUPFL_ADP_FILE = 'KKUPFL_2023_2024_Mock_ADP.xlsx'
KKUPFL_SCORING_FILE = 'KKUPFL_2023_2024_Scoring.xlsx'
DOM_PROJECTIONS_FILE = 'Dom_2023_2024_rankings.xlsx'
EP_PROJECTIONS_FILE = 'EP_202324.xlsx'


# https://stackoverflow.com/questions/54976991/python-openpyxl-userwarning-unknown-extension-issue
warnings.simplefilter("ignore")

if __name__ == '__main__':
    avg_ranks = defaultdict(list)

    kkupfl_adp = KKUPFLAdpReader(KKUPFL_ADP_FILE)
    kkupfl_scoring_23 = KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202223")
    kkupfl_scoring_22 = KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202122")
    kkupfl_scoring_21 = KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202021")
    dom_rk = DomReader(DOM_PROJECTIONS_FILE)
    dom_ppg = DomReader(DOM_PROJECTIONS_FILE, rank_col='/GP', ascending=False)
    ep = EliteProspectsReader(EP_PROJECTIONS_FILE)

    pc = ProjectionsController(
        dom_rk,
        dom_ppg,
        kkupfl_adp,
        kkupfl_scoring_23,
        kkupfl_scoring_22,
        kkupfl_scoring_21,
        ep
    )
    pc.compare(
        avg_ranks,
        '^M.* Pac',
        '^R.* Hart',
        '^A.* Lehk',
        '^D.* Lev',
        '^T.* Hall',
        '^J.* Korp',
        '^S.* Bobr',
        '^S.* Durz',
        '^R.* Thom',
        '^T.* Hert',
        '^J.* Sand',
    )
