import argparse
import warnings

from controller import RankingsController, populate_averaged_rankings, write_avg_ranks_to_csv
from input.select_players import KKUPFL_PLAYERS, PA_PLAYERS
from model.league import League
from reader.dom import DomReader
from reader.ep import EliteProspectsReader
from reader.kkupfl_adp import KKUPFLAdpReader
from reader.kkupfl_scoring import KKUPFLScoringReader
from reader.laidlaw import SteveLaidlawReader
from reader.nhl import NHLReader
from reader.schedule import JeffMaiScheduleReader

DOM_KKUPFL_PROJECTIONS_FILE = 'Dom-KKUPFL.xlsx'
# DOM_PA_PROJECTIONS_FILE = '23-24-Dom-Puckin-Around.xlsx'
# EP_PROJECTIONS_FILE = '23-24-Elite-Prospects-Projections.xlsx'
KKUPFL_ADP_FILE = 'KKUPFL-Mock-ADP.xlsx'
KKUPFL_SCORING_FILE = 'KKUPFL-Scoring.xlsx'
# NHL_PROJECTIONS_FILE = '23-24-NHL-Dot-Com-projections.xlsx'
STEVE_LAIDLAW_PROJECTIONS_FILE = 'Steve-Laidlaw.xlsx'
JEFF_MAI_SCHEDULE_READER = 'Jeff-Mai-Schedule.xlsx'

BASE_READERS = [
    KKUPFLAdpReader(KKUPFL_ADP_FILE),
    # EliteProspectsReader(EP_PROJECTIONS_FILE),
    SteveLaidlawReader(STEVE_LAIDLAW_PROJECTIONS_FILE),
    # NHLReader(NHL_PROJECTIONS_FILE)
]

KKUPFL_READERS = [
    DomReader(DOM_KKUPFL_PROJECTIONS_FILE, "kkupfl"),
    DomReader(DOM_KKUPFL_PROJECTIONS_FILE, "kkupfl", rank_col='/GP', ascending=False),
    KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202324"),
    KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202223"),
    KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202122"),
]

PUCKIN_AROUND_READERS = [
    DomReader(DOM_KKUPFL_PROJECTIONS_FILE, "kkupfl"),
    DomReader(DOM_KKUPFL_PROJECTIONS_FILE, "kkupfl", rank_col='/GP', ascending=False),
    KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202324"),
    KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202223"),
    KKUPFLScoringReader(KKUPFL_SCORING_FILE, "202122"),
]


# https://stackoverflow.com/questions/54976991/python-openpyxl-userwarning-unknown-extension-issue
warnings.simplefilter("ignore")


def get_players_list(league: League):
    players = []
    if league == league.KKUPFL:
        players = KKUPFL_PLAYERS
    elif league == league.PUCKIN_AROUND:
        players = PA_PLAYERS
    return players


def get_readers(league: League):
    '''
    Creates a list of readers appropriate for the given league.
    All readers extend BaseReader.
    '''
    readers = BASE_READERS
    if league == league.KKUPFL:
        readers.extend(KKUPFL_READERS)
    elif league == league.PUCKIN_AROUND:
        readers.extend(PUCKIN_AROUND_READERS)
    return readers


def print_players_matching_regexes(league: str):
    '''
    Finds and prints all player rows matching the defined player regexes.
    '''
    name_regexes = get_players_list(league)
    controller = RankingsController(get_readers(league))
    controller.print_matches_for_all_readers(name_regexes)

def write_consolidated_rankings(league: str, averaged_rankings: dict):
    '''
    Generates a final consolidated and weighted average rankings list and writes it to a file.
    '''
    controller = RankingsController(get_readers(league))
    for reader in controller.readers:
        results = controller.get_rows_matching_regexes(reader, ['.*'])
        controller.register_to_averaged_rankings(reader, results, averaged_rankings)
    populate_averaged_rankings(averaged_rankings)
    sorted_players = sorted(averaged_rankings.items(), key=lambda item: item[1]['avg_rk'])
    write_avg_ranks_to_csv(args.league, sorted_players)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--write', action='store_true', help='Write projections.')
    parser.add_argument('-t', '--top', action='store_true', help='Show the top remaining rows in each ranking.  Defaults to top 10.')
    parser.add_argument('count', metavar='N', type=int, nargs='?', default=10, help='Number of rows to return when "-t/--top" flag used.')
    parser.add_argument('league', type=League, choices=list(League), help='The league the projections are for')

    args = parser.parse_args()
    league = args.league
    averaged_rankings = dict()

    if args.write:
        write_consolidated_rankings(league, averaged_rankings=averaged_rankings)
    else:
        print_players_matching_regexes(league)
