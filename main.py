import argparse
import warnings
from pprint import pprint

from pandas import DataFrame

from controller.projections import ProjectionsController
from service.projections import ProjectionsSvc, populate_averaged_rankings, write_avg_ranks_to_csv
from input.common import *
from input.drafted_kkupfl import KKUPFL_DRAFTED
from input.drafted_pa import PA_DRAFTED
from model.kind import ReaderKind
from model.rank import Rank
from model.league import League


# https://stackoverflow.com/questions/54976991/python-openpyxl-userwarning-unknown-extension-issue
warnings.simplefilter("ignore")


def expand_position_rgx(pos_rgx: str) -> str:
    pos_rgx = pos_rgx.upper()
    if pos_rgx == "F":
        return "C|LW|RW"
    if pos_rgx == "SKT":
        return "C|LW|RW|D"
    return pos_rgx


def get_position_regex(cli_positions: str) -> str:
    if PLAYERS_TO_COMPARE:  # quick compares override any position filters
        return '.*'
    if cli_positions is None:
        return ".*"

    positions = cli_positions.split(",")
    positions_rgx = "|".join([expand_position_rgx(p) for p in positions])
    return positions_rgx

def print_header(header: str) -> None:
    chars = len(header)
    border = '=' * chars
    print(f"{border}\n{header}\n{border}")

def print_results(results: str, count: int):
    '''
    Print results for the current reader
    '''
    print_header()
    print(f"({count} players)")
    print(results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--write', action='store_true', help='Write projections.')
    parser.add_argument('-c', '--count', dest='count', type=int, nargs='?', default=-1, help='Number of rows to return. If omitted, will return all matching rows.')
    parser.add_argument('-t', '--top', dest='top', action=argparse.BooleanOptionalAction, help='Flag to list top matches available rather than filter by regexes')
    parser.add_argument('--feature', action=argparse.BooleanOptionalAction)
    parser.add_argument('-e', '--exclude', dest='excluded', type=str, nargs='?', help='The player regexes to excluded from the search.')
    parser.add_argument('-r', '--regexes', dest='regexes', type=str, nargs='?', help='The player regexes to search upon.')
    parser.add_argument('-p', '--position', dest='positions', type=str, nargs='?', help='The positions to filter upon.')
    parser.add_argument('league', type=League, choices=list(League), help='The league the projections are for')

    args = parser.parse_args()
    league = args.league
    count = args.count
    # regexes = get_player_rgxs(league, args.regexes, args.top)
    # excluded = get_excluded_for_league(league, args.regexes)
    excluded = args.excluded
    positions_rgx = get_position_regex(args.positions)

    averaged_rankings = dict()

    controller = ProjectionsController(args.league)

    # if args.write:
        # write_consolidated_rankings(league, final_rankings)
        # controller = ProjectionsSvc(get_readers(league))
        # write_consolidated_rankings(controller, league, averaged_rankings=averaged_rankings)
    if args.top:
        rankings, count = controller.get_top_rankings(count=count, cli_excluded=excluded)
        print_results(rankings, count)
    # else:
        # projections_controller = ProjectionsSvc(readers=[r for r in get_readers(league) if r.kind == ReaderKind.PROJECTION])
        # historical_controller = ProjectionsSvc(readers=[r for r in get_readers(league) if r.kind == ReaderKind.HISTORICAL])
        # projections = get_projections_by_regexes(projections_controller, historical_controller, regexes)

        # projections_controller.print_matches_for_all_readers(projections)
        # historical_controller.print_matches_for_all_readers(historical_stats_by_reader)
        # print("==================")
        # print("SLEEPERS (shhhhhh)")
        # print("==================")
        # pprint([ x for x in SLEEPERS if x not in KKUPFL_DRAFTED ])
        # print()
