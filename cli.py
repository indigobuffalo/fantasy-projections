import argparse
import warnings

from controller.projections import ProjectionsController
from model.league import League


# https://stackoverflow.com/questions/54976991/python-openpyxl-userwarning-unknown-extension-issue
warnings.simplefilter("ignore")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--write', action='store_true', help='Write projections.')
    parser.add_argument('-l', '--limit', dest='limit', type=int, nargs='?', default=-1, help='Number of rows to return. If omitted, will return all matching rows.')
    parser.add_argument('--feature', action=argparse.BooleanOptionalAction)
    parser.add_argument('-e', '--exclude', dest='exclude', type=str, nargs='?', help='The player regexes to excluded from the search.')
    parser.add_argument('-i', '--include', dest='include', type=str, nargs='?', help='The player regexes to search upon.')
    parser.add_argument('-p', '--position', dest='position', type=str, nargs='?', help='The positions to filter upon.')
    parser.add_argument('league', type=str, help='The league the projections are for.')
    parser.add_argument('season', type=str, help='The season the projections are for.')

    args = parser.parse_args()
    league = args.league
    limit = args.limit
    included = args.include
    excluded = args.exclude
    positions = args.position
    # positions_rgx = get_position_regex(args.positions)

    averaged_rankings = dict()

    controller = ProjectionsController(league=args.league, season=args.season, limit=args.limit)

    if args.write:
        pass
        # write_consolidated_rankings(league, final_rankings)
        # controller = ProjectionsSvc(get_readers(league))
        # write_consolidated_rankings(controller, league, averaged_rankings=averaged_rankings)
    else:
        controller.print_rankings(cli_include=included, cli_exclude=excluded, positions=positions)
        # projections_controller.print_matches_for_all_readers(projections)
        # historical_controller.print_matches_for_all_readers(historical_stats_by_reader)
        # print("==================")
        # print("SLEEPERS (shhhhhh)")
        # print("==================")
        # pprint([ x for x in SLEEPERS if x not in KKUPFL_DRAFTED ])
        # print()
