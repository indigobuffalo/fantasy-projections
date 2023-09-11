from reader.base import FantasyBaseReader
from reader.dom import DomReader
from reader.kkupfl_adp import KKUPFLAdpReader
from reader.kkupfl_scoring import KKUPFLScoringReader

KKUPFL_ADP_FILE = 'KKUPFL_2023_2024_Mock_ADP.xlsx'
KKUPFL_SCORING_FILE = 'KKUPFL_2023_2024_Scoring.xlsx'
DOM_PROJECTIONS_FILE = 'Dom_2023_2024_rankings.xlsx'


class ProjectionsController:
    def __init__(self, *readers: FantasyBaseReader):
        self.readers = readers

    def compare(self, *players: str):
        for r in self.readers:
            print(r)
            res = r.get_players(*players)
            print(f"({len(res)} players)")
            print(res.to_string(index=False))


if __name__ == '__main__':
    kkupfl_adp = KKUPFLAdpReader(KKUPFL_ADP_FILE)
    kkupfl_scoring_23 = KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202223")
    kkupfl_scoring_22 = KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202122")
    kkupfl_scoring_21 = KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202021")
    dom_rk = DomReader(DOM_PROJECTIONS_FILE)
    dom_ppg = DomReader(DOM_PROJECTIONS_FILE, rank_col='/GP', ascending=False)

    pc = ProjectionsController(
        dom_rk,
        dom_ppg,
        kkupfl_adp,
        kkupfl_scoring_23,
        kkupfl_scoring_22,
        kkupfl_scoring_21
    )
    pc.compare(
        '^V.* Husso',
        '^D.* Levi',
        '^C.* Hart',
        '^D.* Mercer',
        '^L.* Couture',
        '^D.* Perron',
        '^R.* Smith',
        '^R.* Hartman',
        '^J.* Vrana',
        '^D.* Strome',
    )
