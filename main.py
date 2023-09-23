import argparse
import warnings

from controller import RankingsController, populate_average_rank, write_avg_ranks_to_csv
from input.input import kkupfl_players, pa_players
from model.league import League
from reader.dom import DomReader
from reader.ep import EliteProspectsReader
from reader.kkupfl_adp import KKUPFLAdpReader
from reader.kkupfl_scoring import KKUPFLScoringReader
from reader.laidlaw import SteveLaidlawReader
from reader.nhl import NHLReader
from reader.schedule import JeffMaiScheduleReader

DOM_KKUPFL_PROJECTIONS_FILE = '23-24-Dom-KKUPFL.xlsx'
DOM_PA_PROJECTIONS_FILE = '23-24-Dom-Puckin-Around.xlsx'
EP_PROJECTIONS_FILE = '23-24-Elite-Prospects-Projections.xlsx'
KKUPFL_ADP_FILE = '23-24-KKUPFL-Mock-ADP.xlsx'
KKUPFL_SCORING_FILE = '23-24-KKUPFL-Scoring.xlsx'
NHL_PROJECTIONS_FILE = '23-24-NHL-Dot-Com-projections.xlsx'
STEVE_LAIDLAW_PROJECTIONS_FILE = '23-24-Steve-Laidlaw-Projections.xlsx'
JEFF_MAI_SCHEDULE_READER = '23-24-Jeff-Mai-Schedule.xlsx'


# https://stackoverflow.com/questions/54976991/python-openpyxl-userwarning-unknown-extension-issue
warnings.simplefilter("ignore")


def get_players_list(league: League):
    players = []
    if league == league.KKUPFL:
        players = kkupfl_players
    elif league == league.PUCKIN_AROUND:
        players = pa_players
    return players


def get_readers(league: League, schedule=True):
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
    if schedule:
        readers.append(JeffMaiScheduleReader(JEFF_MAI_SCHEDULE_READER, sheet_name="Games per week"))
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

    players = get_players_list(args.league)

    if args.write:
        controller = RankingsController(get_readers(args.league, schedule=False))
        controller.compare_players(aggregated_ranks, teams, ['.*'], write=True)
        populate_average_rank(aggregated_ranks)
        sorted_players = sorted(aggregated_ranks.items(), key=lambda item: item[1]['avg_rk'])
        write_avg_ranks_to_csv(args.league, sorted_players)
    else:
        controller = RankingsController(get_readers(args.league))
        controller.compare_players(aggregated_ranks, teams, players)
