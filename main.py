import argparse
import warnings

from pandas import DataFrame

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
    EliteProspectsReader(FantasyConfig.projection_files.ELITE_PROSPECTS),
    SteveLaidlawReader(FantasyConfig.projection_files.STEVE_LAIDLAW),
    # NHLReader(NHL_PROJECTIONS_FILE)
]


KKUPFL_READERS = [
    BlakeRedditReader(FantasyConfig.projection_files.BLAKE_KKUPFL),
    DomReader(FantasyConfig.projection_files.DOM_KKUPFL),
    DomReader(FantasyConfig.projection_files.DOM_KKUPFL, rank_col='/GP', ascending=False),
    KKUPFLScoringReader(FantasyConfig.projection_files.KKUPFL_SCORING, "202324"),
    KKUPFLScoringReader(FantasyConfig.projection_files.KKUPFL_SCORING, "202223"),
]


PUCKIN_AROUND_READERS = [
   DomReader(FantasyConfig.projection_files.DOM_PA),
   DomReader(FantasyConfig.projection_files.DOM_PA, rank_col='/GP', ascending=False),
   KKUPFLScoringReader(FantasyConfig.projection_files.KKUPFL_SCORING, "202324"),
   KKUPFLScoringReader(FantasyConfig.projection_files.KKUPFL_SCORING, "202223"),
]


# https://stackoverflow.com/questions/54976991/python-openpyxl-userwarning-unknown-extension-issue
warnings.simplefilter("ignore")


def _parse_cmd_line_regexes(cli_rgxs: str) -> list[str]:
    return cli_rgxs.split(",")


def get_player_rgxs(league: League, cli_rgxs = None) -> list[str]:
    players = []
    if cli_rgxs is not None:
        players = _parse_cmd_line_regexes(cli_rgxs)
    elif len(QUICK_COMPARE_PLAYERS) >= 1:
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


def _trim_results(results: DataFrame, count: int):
    return results.head(count)


def refine_results(results: DataFrame, count: int = -1) -> DataFrame:
    if count > 0:
        results = _trim_results(results, count)
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--write', action='store_true', help='Write projections.')
    parser.add_argument('-c', '--count', dest='count', type=int, nargs='?', default=-1, help='Number of rows to return. If omitted, will return all matching rows.')
    parser.add_argument('-r', '--regexes', dest='regexes', type=str, nargs='?', help='The player regexes to search upon.')
    parser.add_argument('league', type=League, choices=list(League), help='The league the projections are for')

    args = parser.parse_args()
    league = args.league
    count = args.count
    regexes = args.regexes

    controller = RankingsController(get_readers(league))
    averaged_rankings = dict()

    if args.write:
        write_consolidated_rankings(controller, league, averaged_rankings=averaged_rankings)
    else:
        results_by_reader = controller.get_matches_for_all_readers(get_player_rgxs(league, cli_rgxs=regexes))
        for rd, res in results_by_reader.items():
            results_by_reader[rd] = refine_results(res, count=count)
        controller.print_matches_for_all_readers(results_by_reader)
