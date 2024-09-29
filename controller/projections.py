from typing import Tuple
from config.config import FantasyConfig
from pandas import DataFrame
from data.dynamic.drafted import KKUPFL_DRAFTED, PA_DRAFTED
from data.dynamic.filters import PLAYERS_TO_COMPARE
from model.league import League
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
        count: int = -1
    ):
        self.league = League(league)
        self.count = count
    
    def write_consolidated_rankings(league: str, final_rankings: dict):
        controller = ProjectionsSvc(get_daos(league))
        write_consolidated_rankings(controller, league, averaged_rankings=averaged_rankings)
    
    def get_exclude_rgxs(self, player_rgxs: str = None) -> list[str]:
        """Get list of comma-delimited player regexes to exclude from results
    
        Args:
            player_rgxs (str): Comma-delimited player regexes
    
        Returns:
            list[str]: List of players to exclude
        """
        excluded = list()
        if player_rgxs is not None:
            excluded.extend(player_rgxs.split(","))

        if self.league == League.KKUPFL:
            excluded.extend(KKUPFL_DRAFTED)
        elif self.league == League.PUCKIN_AROUND:
            excluded.extend(PA_DRAFTED)

        return excluded
    
    @staticmethod
    def get_include_rgxs(rgxs: str = None, top: bool = False) -> list[str]:
        if rgxs is not None:
            return rgxs.split(",")
        elif top:
            return ['.*']
        else:
            return PLAYERS_TO_COMPARE

    def get_top_rankings(self, cli_include: str, cli_exclude: str) -> Tuple[str, int]:
        excluded = self.get_exclude_rgxs(player_rgxs=cli_exclude)
        included = self.get_include_rgxs(cli_include, self.count > 0)
        print(f"Excluded: {excluded}")
        print(f"Included: {included}")
        import ipdb; ipdb.set_trace()
        pass
