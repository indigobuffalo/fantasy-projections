import argparse
import warnings

from pandas import DataFrame

from config.config import FantasyConfig
from controller import RankingsController, populate_averaged_rankings, write_avg_ranks_to_csv
from input.player_rgxs import *
from input.drafted_kkupfl import KKUPFL_DRAFTED
from input.drafted_pa import PA_DRAFTED
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

    if len(players) == 0:
        players = [".*"]

    return players


def expand_position_rgx(pos_rgx: str) -> str:
    pos_rgx = pos_rgx.upper()
    if pos_rgx == "F":
        return "C|LW|RW"
    if pos_rgx == "SKT":
        return "C|LW|RW|D"
    return pos_rgx


def get_position_regex(cli_positions: str) -> str:
    if cli_positions is None:
        return ".*"

    positions = cli_positions.split(",")
    positions_rgx = "|".join([ expand_position_rgx(p) for p in positions ])
    return positions_rgx
    

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


def write_consolidated_rankings(controller: RankingsController, league: str, averaged_rankings: dict):
    '''
    Generates a final consolidated and weighted average rankings list and writes it to a file.
    '''
    for reader in controller.readers:
        results = controller.get_matches(reader)
        controller.register_to_averaged_rankings(reader, results, averaged_rankings)
    populate_averaged_rankings(averaged_rankings)
    sorted_players = sorted(averaged_rankings.items(), key=lambda item: item[1]['avg_rk'])
    write_avg_ranks_to_csv(league, sorted_players)


def get_excluded_for_league(league: str) -> list[str]:
    """Get list of players to exclude from results

    Args:
        league (str): Fantasy league

    Returns:
        list[str]: List of players to exclude
    """
    excluded = list()
    if league == League.KKUPFL:
        excluded = KKUPFL_DRAFTED
    elif league == League.PUCKIN_AROUND:
        excluded = PA_DRAFTED
    return excluded


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--write', action='store_true', help='Write projections.')
    parser.add_argument('-c', '--count', dest='count', type=int, nargs='?', default=-1, help='Number of rows to return. If omitted, will return all matching rows.')
    parser.add_argument('-r', '--regexes', dest='regexes', type=str, nargs='?', help='The player regexes to search upon.')
    parser.add_argument('-p', '--position', dest='positions', type=str, nargs='?', help='The positions to filter upon.')
    parser.add_argument('league', type=League, choices=list(League), help='The league the projections are for')

    args = parser.parse_args()
    league = args.league
    count = args.count
    regexes = get_player_rgxs(league, args.regexes)
    excluded = get_excluded_for_league(league)
    positions_rgx = get_position_regex(args.positions)

    controller = RankingsController(get_readers(league))
    averaged_rankings = dict()

    if args.write:
        write_consolidated_rankings(controller, league, averaged_rankings=averaged_rankings)
    else:
        results_by_reader = controller.get_matches_for_all_readers(regexes)
        for rd, res in results_by_reader.items():
            results_by_reader[rd] = controller.refine_results(rd, res, positions_rgx=positions_rgx, excluded=excluded, count=count)
        controller.print_matches_for_all_readers(results_by_reader)
