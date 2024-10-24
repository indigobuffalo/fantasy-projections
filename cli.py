import argparse
import warnings
from pprint import pprint

from pandas import DataFrame

from config.config import FantasyConfig
from service.projections import ProjectionsSvc, populate_averaged_rankings, write_avg_ranks_to_csv
from input.player_rgxs import *
from input.drafted_kkupfl import KKUPFL_DRAFTED
from input.drafted_pa import PA_DRAFTED
from model.kind import ReaderKind
from model.league import League
from model.rank import Rank
from dao.base import FantasyBaseDao
from dao.blake import BlakeRedditDao
from dao.dom import DomDao
from dao.ep import EliteProspectsDao
from dao.kkupfl_adp import KKUPFLAdpDao
from dao.kkupfl_scoring import KKUPFLScoringDao
from dao.laidlaw import SteveLaidlawDao
from dao.nhl import NHLDao
from dao.schedule import JeffMaiScheduleDao

BASE_READERS = [
    KKUPFLAdpDao(FantasyConfig.projection_files.KKUPFL_ADP),
    EliteProspectsDao(FantasyConfig.projection_files.ELITE_PROSPECTS),
    SteveLaidlawDao(FantasyConfig.projection_files.STEVE_LAIDLAW),
]

KKUPFL_READERS = [
    BlakeRedditDao(FantasyConfig.projection_files.BLAKE_KKUPFL),
    DomDao(FantasyConfig.projection_files.DOM_KKUPFL),
    DomDao(FantasyConfig.projection_files.DOM_KKUPFL, rank_col='/GP', ascending=False),
    KKUPFLScoringDao(FantasyConfig.projection_files.KKUPFL_SCORING, "202324"),
    KKUPFLScoringDao(FantasyConfig.projection_files.KKUPFL_SCORING, "202223"),
    KKUPFLScoringDao(FantasyConfig.projection_files.KKUPFL_SCORING, "202122"),
]

PUCKIN_AROUND_READERS = [
    DomDao(FantasyConfig.projection_files.DOM_PA),
    DomDao(FantasyConfig.projection_files.DOM_PA, rank_col='/GP', ascending=False),
    KKUPFLScoringDao(FantasyConfig.projection_files.KKUPFL_SCORING, "202324"),
    KKUPFLScoringDao(FantasyConfig.projection_files.KKUPFL_SCORING, "202223"),
]

# https://stackoverflow.com/questions/54976991/python-openpyxl-userwarning-unknown-extension-issue
warnings.simplefilter("ignore")


def _parse_cmd_line_regexes(cli_rgxs: str) -> list[str]:
    return cli_rgxs.split(",")


def get_player_rgxs(league: League, cli_rgxs: str= None, top: bool = False) -> list[str]:
    players = ['.*']
    if cli_rgxs is not None:
        players = _parse_cmd_line_regexes(cli_rgxs)
    elif top:
        return players
    elif len(QUICK_COMPARE_PLAYERS) >= 1:
        players = QUICK_COMPARE_PLAYERS
    elif league == league.KKUPFL:
        players = KKUPFL_PLAYERS
    elif league == league.PUCKIN_AROUND:
        players = PA_PLAYERS

    return players


def get_excluded_for_league(league: str, cli_rgxs: str = None) -> list[str]:
    """Get list of players to exclude from results

    Args:
        league (str): Fantasy league

    Returns:
        list[str]: List of players to exclude
    """
    excluded = list()
    if cli_rgxs is not None:
        return excluded
    elif QUICK_COMPARE_PLAYERS:  # quick compares override any exclusions
        return excluded
    elif league == League.KKUPFL:
        excluded = KKUPFL_DRAFTED
    elif league == League.PUCKIN_AROUND:
        excluded = PA_DRAFTED
    return excluded


def expand_position_rgx(pos_rgx: str) -> str:
    pos_rgx = pos_rgx.upper()
    if pos_rgx in ["F", "FWD"]:
        return "C|LW|RW"
    if pos_rgx == "SKT":
        return "C|LW|RW|D"
    return pos_rgx


def get_position_regex(cli_positions: str) -> str:
    if QUICK_COMPARE_PLAYERS:  # quick compares override any position filters
        return '.*'
    if cli_positions is None:
        return ".*"

    positions = cli_positions.split(",")
    positions_rgx = "|".join([expand_position_rgx(p) for p in positions])
    return positions_rgx


def get_readers(league: League) -> list[FantasyBaseDao]:
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


def write_consolidated_rankings(controller: ProjectionsSvc, league: str,
                                averaged_rankings: dict):
    '''
    Generates a final consolidated and weighted average rankings list and writes it to a file.
    '''
    for reader in controller.readers:
        results = controller.get_matches(reader)
        controller.register_to_averaged_rankings(reader, results,
                                                 averaged_rankings)
    populate_averaged_rankings(averaged_rankings)
    sorted_players = sorted(averaged_rankings.items(),
                            key=lambda item: item[1]['avg_rk'])
    write_avg_ranks_to_csv(league, sorted_players)


def get_projections_by_regexes(proj_controller: ProjectionsSvc, historical_controller: ProjectionsSvc, regexes: list[str]) -> dict[FantasyBaseDao, DataFrame]:
    matched_players = set()
    projections_by_reader = proj_controller.get_matches_for_readers(regexes)
    for reader, results in projections_by_reader.items():
        projections_by_reader[reader] = proj_controller.refine_results(
            reader,
            results,
            positions_rgx=positions_rgx,
            excluded=excluded,
            count=count)
        matched_players.update(projections_by_reader[reader][reader.primary_col].tolist())

    historical_stats_by_reader = historical_controller.get_matches_for_readers(matched_players)
    return projections_by_reader | historical_stats_by_reader


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--write', action='store_true', help='Write projections.')
    parser.add_argument('-c', '--count', dest='count', type=int, nargs='?', default=-1, help='Number of rows to return. If omitted, will return all matching rows.')
    parser.add_argument('-t', '--top', dest='top', action=argparse.BooleanOptionalAction, help='Flag to list top matches available rather than filter by regexes')
    parser.add_argument('--feature', action=argparse.BooleanOptionalAction)
    parser.add_argument('-r', '--regexes', dest='regexes', type=str, nargs='?', help='The player regexes to search upon.')
    parser.add_argument('-p', '--position', dest='positions', type=str, nargs='?', help='The positions to filter upon.')
    parser.add_argument('league', type=League, choices=list(League), help='The league the projections are for')

    args = parser.parse_args()
    league = args.league
    count = args.count
    regexes = get_player_rgxs(league, args.regexes, args.top)
    excluded = get_excluded_for_league(league, args.regexes)
    positions_rgx = get_position_regex(args.positions)

    averaged_rankings = dict()

    if args.write:
        # write_consolidated_rankings(league, final_rankings)
        controller = ProjectionsSvc(get_readers(league))
        write_consolidated_rankings(controller, league, averaged_rankings=averaged_rankings)
    else:
        projections_controller = ProjectionsSvc(readers=[r for r in get_readers(league) if r.kind == ReaderKind.PROJECTION])
        historical_controller = ProjectionsSvc(readers=[r for r in get_readers(league) if r.kind == ReaderKind.HISTORICAL])
        projections = get_projections_by_regexes(projections_controller, historical_controller, regexes)

        projections_controller.print_matches_for_all_readers(projections)
        # historical_controller.print_matches_for_all_readers(historical_stats_by_reader)
        print("==================")
        print("SLEEPERS (shhhhhh)")
        print("==================")
        pprint([ x for x in SLEEPERS if x not in PA_DRAFTED])
        print()
