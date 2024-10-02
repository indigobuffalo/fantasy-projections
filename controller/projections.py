import stat
from typing import Tuple
from config.config import FantasyConfig
from pandas import DataFrame
from data.dynamic.drafted import KKUPFL_DRAFTED, PA_DRAFTED
from data.dynamic.filters import DO_NOT_DRAFT, PLAYERS_TO_COMPARE
from model.league import League
from model.season import Season
from service.projections import ProjectionsSvc


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


class ProjectionsController:
    def __init__(
        self, 
        league: str, 
        season: str,
        limit: int = -1
    ):
        self.league = League(league)
        self.season = Season(season)
        self.limit = limit 
        self.service = ProjectionsSvc(self.league, self.season)
    
    def write_consolidated_rankings(league: str, final_rankings: dict):
        controller = ProjectionsSvc(get_daos(league))
        write_consolidated_rankings(controller, league, averaged_rankings=averaged_rankings)
    
    def _get_exclude_rgxs(self, player_rgxs: str = None) -> list[str]:
        """Get list of comma-delimited player regexes to exclude from results
    
        Args:
            player_rgxs (str): Comma-delimited player regexes
    
        Returns:
            list[str]: List of players to exclude
        """
        excluded = list(DO_NOT_DRAFT)

        if player_rgxs is not None:
            excluded.extend(player_rgxs.split(","))

        if self.league == League.KKUPFL:
            excluded.extend(KKUPFL_DRAFTED)
        elif self.league == League.PUCKIN_AROUND:
            excluded.extend(PA_DRAFTED)

        return excluded
    
    def _get_include_rgxs(self, rgxs: str = None) -> list[str]:
        if rgxs is not None:
            return rgxs.split(",")
        elif self.limit > 0:  # limit implies we just care about the top N rankings per analyst
            return ['.*']
        else:
            return PLAYERS_TO_COMPARE

    @staticmethod
    def _get_position_rgxs(positions: str) -> list[str]:
        # TODO: consider making this a default in argparse
        if positions is None:
            return [".*"]

        positions = [p.upper() for p in positions.split(",")]
        pos_map = {
            "F": "C|LW|RW",
            "FWD": "C|LW|RW",
            "SKT": "C|LW|RW|D",
        }
        return [pos_map.get(p, p) for p in positions]

    @staticmethod
    def _get_title(results_metadata: str):
        title_parts = results_metadata.split("__")
        title_parts[-1] = f"({title_parts[-1]})"
        return " ".join(title_parts)

    def print_header(self, results_metadata: str):
        title = self._get_title(results_metadata)
        chars = len(title)
        border = '=' * chars
        print(f"{border}\n{title}\n{border}")

    def print(self, results_metadata:str, results: DataFrame) -> None:
        '''
        Print results for the current reader
        '''
        self.print_header(results_metadata)
        print(f"({len(results)} players)")
        print(results.to_string(index=False))

    def print_rankings(self, cli_include: str, cli_exclude: str, positions: str = None) -> Tuple[str, int]:
        included_primary = self._get_include_rgxs(cli_include)
        excluded_primary = None if cli_include is not None else self._get_exclude_rgxs(cli_exclude)
        included_pos = self._get_position_rgxs(positions)
        results = self.service.get_rankings(primary_rgxs=included_primary, primary_filter_rgxs=excluded_primary, pos_rgxs=included_pos, limit=self.limit)
        for result_metadata, result in results.items():
            self.print(result_metadata, result)
