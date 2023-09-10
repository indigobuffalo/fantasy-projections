from reader.base import FantasyBaseReader
from reader.dom import DomReader
from reader.kkupfl import KKUPFLAdpReader

KKUPFL_ADP_FILE = 'KKUPFL_2023_2024_Mock_ADP.xlsx'
DOM_PROJECTIONS_FILE = 'Dom_2023_2024_rankings.xlsx'


class ProjectionsController:
    def __init__(self, *readers: FantasyBaseReader):
        self.readers = readers

    def compare(self, *players: str):
        for r in self.readers:
            print(r)
            res = r.get_players(*players)
            print(res.to_string(index=False))


if __name__ == '__main__':
    kkupfl = KKUPFLAdpReader(KKUPFL_ADP_FILE)
    dom = DomReader(DOM_PROJECTIONS_FILE)

    pc = ProjectionsController(dom, kkupfl)
    pc.compare(
        'T.*Chabo',
        'J.*Sand',
        'S.*Jones',
        'N.*Dobs',
        'B.*Burn'
    )
