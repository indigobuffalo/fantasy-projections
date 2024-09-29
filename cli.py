import argparse
import warnings
from pprint import pprint

from controller.projections import ProjectionsController
from model.league import League


# https://stackoverflow.com/questions/54976991/python-openpyxl-userwarning-unknown-extension-issue
warnings.simplefilter("ignore")


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
    parser.add_argument('-e', '--exclude', dest='exclude', type=str, nargs='?', help='The player regexes to excluded from the search.')
    parser.add_argument('-i', '--include', dest='include', type=str, nargs='?', help='The player regexes to search upon.')
    parser.add_argument('-p', '--position', dest='positions', type=str, nargs='?', help='The positions to filter upon.')
    parser.add_argument('league', type=str, help='The league the projections are for')

    args = parser.parse_args()
    league = args.league
    count = args.count
    # regexes = get_player_rgxs(league, args.regexes, args.top)
    # excluded = get_excluded_for_league(league, args.regexes)
    included = args.include
    excluded = args.exclude
    # positions_rgx = get_position_regex(args.positions)

    averaged_rankings = dict()

    controller = ProjectionsController(league=args.league, count=args.count)

    # if args.write:
        # write_consolidated_rankings(league, final_rankings)
        # controller = ProjectionsSvc(get_readers(league))
        # write_consolidated_rankings(controller, league, averaged_rankings=averaged_rankings)
    if args.top:
        rankings = controller.get_top_rankings(cli_include=included, cli_exclude=excluded)
        print_results(rankings)
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
