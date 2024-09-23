from ast import Tuple
from config.config import FantasyConfig
from dao.base import FantasyBaseDao
from dao.blake import BlakeRedditDao
from dao.dom import DomDao
from dao.ep import EliteProspectsDao
from dao.kkupfl_adp import KKUPFLAdpDao
from dao.kkupfl_scoring import KKUPFLScoringDao
from dao.laidlaw import SteveLaidlawDao
from pandas import DataFrame
# from dao.nhl import NHLDao
# from dao.schedule import JeffMaiScheduleDao
from input.drafted_kkupfl import KKUPFL_DRAFTED
from input.drafted_pa import PA_DRAFTED
from model.league import League
from service.projection.base import get_excluded
from service.projections import ProjectionsSvc


BASE_DAOS = [
    KKUPFLAdpDao(FantasyConfig.projection_files.KKUPFL_ADP),
    EliteProspectsDao(FantasyConfig.projection_files.ELITE_PROSPECTS),
    SteveLaidlawDao(FantasyConfig.projection_files.STEVE_LAIDLAW),
]


KKUPFL_DAOS = [
    BlakeRedditDao(FantasyConfig.projection_files.BLAKE_KKUPFL),
    DomDao(FantasyConfig.projection_files.DOM_KKUPFL),
    DomDao(FantasyConfig.projection_files.DOM_KKUPFL, rank_col='/GP', ascending=False),
    KKUPFLScoringDao(FantasyConfig.projection_files.KKUPFL_SCORING, "202324"),
    KKUPFLScoringDao(FantasyConfig.projection_files.KKUPFL_SCORING, "202223"),
    KKUPFLScoringDao(FantasyConfig.projection_files.KKUPFL_SCORING, "202122"),
]


PUCKIN_AROUND_DAOS = [
    DomDao(FantasyConfig.projection_files.DOM_PA),
    DomDao(FantasyConfig.projection_files.DOM_PA, rank_col='/GP', ascending=False),
    KKUPFLScoringDao(FantasyConfig.projection_files.KKUPFL_SCORING, "202324"),
    KKUPFLScoringDao(FantasyConfig.projection_files.KKUPFL_SCORING, "202223"),
]

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


def get_daos(league: League) -> list[FantasyBaseDao]:
    '''
    Creates a list of readers appropriate for the given league.
    All readers extend BaseReader.
    '''
    readers = BASE_DAOS
    if league == league.KKUPFL:
        readers.extend(KKUPFL_DAOS)
    elif league == league.PUCKIN_AROUND:
        readers.extend(PUCKIN_AROUND_DAOS)
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


class ProjectionsController:
    def __init__(self, league: str = None):
        self.league = League[league] if league is not None else None
    
    def write_consolidated_rankings(league: str, final_rankings: dict):
        controller = ProjectionsSvc(get_daos(league))
        write_consolidated_rankings(controller, league, averaged_rankings=averaged_rankings)
    
    def get_excluded(self, player_rgxs: str = None) -> list[str]:
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
    
    def get_player_rgxs(league: League, cli_rgxs: str= None, top: bool = False) -> list[str]:
        players = ['.*']
        if cli_rgxs is not None:
            players = cli_rgxs.split(",")
        elif top:
            return players
        elif len(QUICK_COMPARE_PLAYERS) >= 1:
            players = QUICK_COMPARE_PLAYERS
        elif league == league.KKUPFL:
            players = KKUPFL_PLAYERS
        elif league == league.PUCKIN_AROUND:
            players = PA_PLAYERS

        return players

    def get_top_rankings(self, count: int, cli_excluded: str) -> Tuple[str, int]:
        excluded = self.get_excluded(player_rgxs=cli_excluded)
        included = get_player_rgxs


        pass