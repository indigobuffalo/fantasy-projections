import argparse
import warnings

from controller import RankingsController, populate_average_rank, write_avg_ranks_to_csv
from enum import Enum
from input import all_players, select_players
from reader.dom import DomReader
from reader.ep import EliteProspectsReader
from reader.kkupfl_adp import KKUPFLAdpReader
from reader.kkupfl_scoring import KKUPFLScoringReader
from reader.laidlaw import SteveLaidlawReader

DOM_KKUPFL_PROJECTIONS_FILE = 'Dom_2023_2024_KKUPFL.xlsx'
DOM_PA_PROJECTIONS_FILE = 'Dom_2023_2024_Puckin_Around.xlsx'
EP_PROJECTIONS_FILE = 'EP_202324.xlsx'
KKUPFL_ADP_FILE = 'KKUPFL_2023_2024_Mock_ADP.xlsx'
KKUPFL_SCORING_FILE = 'KKUPFL_2023_2024_Scoring.xlsx'
STEVE_LAIDLAW_PROJECTIONS_FILE = 'Steve_Laidlaw_2023_24.xlsx'


# https://stackoverflow.com/questions/54976991/python-openpyxl-userwarning-unknown-extension-issue
warnings.simplefilter("ignore")


class League(Enum):
    ANY = 'any'
    KKUPFL = 'kkupfl'
    PUCKIN_AROUND = 'pa'

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented


def get_readers(league):
    readers = [
        KKUPFLAdpReader(KKUPFL_ADP_FILE),
        EliteProspectsReader(EP_PROJECTIONS_FILE),
        SteveLaidlawReader(STEVE_LAIDLAW_PROJECTIONS_FILE)
    ]
    if league == league.KKUPFL:
        readers.extend([
            KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202223"),
            KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202122"),
            KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202021"),
            DomReader(DOM_KKUPFL_PROJECTIONS_FILE, "kkupfl"),
            DomReader(DOM_KKUPFL_PROJECTIONS_FILE, "kkupfl", rank_col='/GP', ascending=False)
        ])
    elif league == league.PUCKIN_AROUND:
        readers.extend([
            DomReader(DOM_PA_PROJECTIONS_FILE, "puckin around"),
            DomReader(DOM_PA_PROJECTIONS_FILE, "puckin around", rank_col='/GP', ascending=False)
        ])
    return readers


if __name__ == '__main__':
    aggregated_ranks = dict()
    teams = set()

    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--write', action='store_true', help='Write rankings.')
    parser.add_argument('-t', '--top', action='store_true', help='Show the top remaining rows in each ranking.  Defaults to top 10.')
    parser.add_argument('count', metavar='N', type=int, nargs='?', default=10, help='Number of rows to return when "-t/--top" flag used.')
    parser.add_argument('league', type=League, choices=list(League), help='The league the rankings are for')

    args = parser.parse_args()
    controller = RankingsController(get_readers(args.league))

    if args.write:
        controller.compare_players(aggregated_ranks, teams, all_players)
        populate_average_rank(aggregated_ranks)
        sorted_players = sorted(aggregated_ranks.items(), key=lambda item: item[1]['avg_rk'])
        write_avg_ranks_to_csv(sorted_players)
    else:
        controller.compare_players(aggregated_ranks, teams, select_players)
        print(teams)

