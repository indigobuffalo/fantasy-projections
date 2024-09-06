import argparse
import warnings

from config.config import FantasyConfig
from controller import RankingsController, populate_averaged_rankings, write_avg_ranks_to_csv
from input.player_rgxs import *
from model.league import League
from reader.blake import BlakeRedditReader
from reader.dom import DomReader
from reader.ep import EliteProspectsReader
from reader.kkupfl_adp import KKUPFLAdpReader
from reader.kkupfl_scoring import KKUPFLScoringReader
from reader.laidlaw import SteveLaidlawReader
from reader.nhl import NHLReader
from reader.schedule import JeffMaiScheduleReader


BASE_READERS = [
    KKUPFLAdpReader(FantasyConfig.projection_files.KKUPFL_ADP),
    # EliteProspectsReader(EP_PROJECTIONS_FILE),
    SteveLaidlawReader(FantasyConfig.projection_files.STEVE_LAIDLAW),
    # NHLReader(NHL_PROJECTIONS_FILE)
]


KKUPFL_READERS = [
    BlakeRedditReader(FantasyConfig.projection_files.BLAKE_KKUPFL),
    DomReader(FantasyConfig.projection_files.DOM_KKUPFL),
    DomReader(FantasyConfig.projection_files.DOM_KKUPFL, rank_col='/GP', ascending=False),
    KKUPFLScoringReader(FantasyConfig.projection_files.KKUPFL_SCORING, "202324"),
    KKUPFLScoringReader(FantasyConfig.projection_files.KKUPFL_SCORING, "202223"),
    KKUPFLScoringReader(FantasyConfig.projection_files.KKUPFL_SCORING, "202122"),
]


PUCKIN_AROUND_READERS = [
   DomReader(FantasyConfig.projection_files.DOM_PA),
   DomReader(FantasyConfig.projection_files.DOM_PA, rank_col='/GP', ascending=False),
   KKUPFLScoringReader(FantasyConfig.projection_files.KKUPFL_SCORING, "202324"),
   KKUPFLScoringReader(FantasyConfig.projection_files.KKUPFL_SCORING, "202223"),
   KKUPFLScoringReader(FantasyConfig.projection_files.KKUPFL_SCORING, "202122"),
]


# https://stackoverflow.com/questions/54976991/python-openpyxl-userwarning-unknown-extension-issue
warnings.simplefilter("ignore")


def get_player_rgxs(league: League):
    players = []
    if len(QUICK_COMPARE_PLAYERS) >= 1:
        players = QUICK_COMPARE_PLAYERS
    elif league == league.KKUPFL:
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


def get_players_matching_regexes(controller: RankingsController, league: str):
    '''
    Gets prints all player rows matching the defined player regexes.
    '''
    name_regexes = get_player_rgxs(league)
    controller.print_matches_for_all_readers(name_regexes)


def print_players_matching_regexes(controller: RankingsController, league: str):
    '''
    Finds and prints all player rows matching the defined player regexes.
    '''
    name_regexes = get_player_rgxs(league)
    controller.print_matches_for_all_readers(name_regexes)


def write_consolidated_rankings(controller: RankingsController, league: str, averaged_rankings: dict):
    '''
    Generates a final consolidated and weighted average rankings list and writes it to a file.
    '''
    for reader in controller.readers:
        results = controller.get_rows_matching_regexes(reader, ['.*'])
        controller.register_to_averaged_rankings(reader, results, averaged_rankings)
    populate_averaged_rankings(averaged_rankings)
    sorted_players = sorted(averaged_rankings.items(), key=lambda item: item[1]['avg_rk'])
    write_avg_ranks_to_csv(league, sorted_players)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--write', action='store_true', help='Write projections.')
    parser.add_argument('-t', '--top', action='store_true', help='Show the top remaining rows in each ranking.  Defaults to top 10.')
    parser.add_argument('count', metavar='N', type=int, nargs='?', default=10, help='Number of rows to return when "-t/--top" flag used.')
    parser.add_argument('league', type=League, choices=list(League), help='The league the projections are for')

    args = parser.parse_args()
    league = args.league
    controller = RankingsController(get_readers(league))
    averaged_rankings = dict()

    if args.write:
        write_consolidated_rankings(controller, league, averaged_rankings=averaged_rankings)
    else:
        reader_results = controller.get_matches_for_all_readers(get_player_rgxs(league))
        controller.print_matches_for_all_readers(reader_results)
