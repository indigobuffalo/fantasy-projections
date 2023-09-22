import argparse
import warnings

from controller import RankingsController, populate_average_rank, write_avg_ranks_to_csv
from input import select_players
from model.league import League
from reader.dom import DomReader
from reader.ep import EliteProspectsReader
from reader.kkupfl_adp import KKUPFLAdpReader
from reader.kkupfl_scoring import KKUPFLScoringReader
from reader.laidlaw import SteveLaidlawReader
from reader.nhl import NHLReader
from reader.schedule import JeffMaiScheduleReader

DOM_KKUPFL_PROJECTIONS_FILE = 'Dom_2023_2024_KKUPFL.xlsx'
DOM_PA_PROJECTIONS_FILE = 'Dom_2023_2024_Puckin_Around.xlsx'
EP_PROJECTIONS_FILE = 'EP_202324.xlsx'
KKUPFL_ADP_FILE = 'KKUPFL_2023_2024_Mock_ADP.xlsx'
KKUPFL_SCORING_FILE = 'KKUPFL_2023_2024_Scoring.xlsx'
NHL_PROJECTIONS_FILE = '23-24-nhl-com-projections.xlsx'
STEVE_LAIDLAW_PROJECTIONS_FILE = 'Steve_Laidlaw_2023_24.xlsx'

JEFF_MAI_SCHEDULE_READER = '23-24-NHL-Schedule-Jeff-Mai.xlsx'


# https://stackoverflow.com/questions/54976991/python-openpyxl-userwarning-unknown-extension-issue
warnings.simplefilter("ignore")


def get_readers(league):
    readers = [
        KKUPFLAdpReader(KKUPFL_ADP_FILE),
        EliteProspectsReader(EP_PROJECTIONS_FILE),
        SteveLaidlawReader(STEVE_LAIDLAW_PROJECTIONS_FILE),
        NHLReader(NHL_PROJECTIONS_FILE)
    ]
    if league == league.KKUPFL:
        readers.extend([
            DomReader(DOM_KKUPFL_PROJECTIONS_FILE, "kkupfl"),
            DomReader(DOM_KKUPFL_PROJECTIONS_FILE, "kkupfl", rank_col='/GP', ascending=False),
            KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202223"),
            KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202122"),
            KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202021"),
        ])
    elif league == league.PUCKIN_AROUND:
        readers.extend([
            DomReader(DOM_PA_PROJECTIONS_FILE, "puckin around"),
            DomReader(DOM_PA_PROJECTIONS_FILE, "puckin around", rank_col='/GP', ascending=False)
        ])
    readers.append(JeffMaiScheduleReader(JEFF_MAI_SCHEDULE_READER))
    return readers


if __name__ == '__main__':
    aggregated_ranks = dict()
    teams = set()

    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--write', action='store_true', help='Write projections.')
    parser.add_argument('-t', '--top', action='store_true', help='Show the top remaining rows in each ranking.  Defaults to top 10.')
    parser.add_argument('count', metavar='N', type=int, nargs='?', default=10, help='Number of rows to return when "-t/--top" flag used.')
    parser.add_argument('league', type=League, choices=list(League), help='The league the projections are for')

    args = parser.parse_args()
    controller = RankingsController(get_readers(args.league))

    if args.write:
        controller.compare_players(aggregated_ranks, teams, ['.*'], verbose=False)
        populate_average_rank(aggregated_ranks)
        sorted_players = sorted(aggregated_ranks.items(), key=lambda item: item[1]['avg_rk'])
        write_avg_ranks_to_csv(args.league, sorted_players)
    else:
        controller.compare_players(aggregated_ranks, teams, select_players)
