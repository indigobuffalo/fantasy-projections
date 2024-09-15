from config.config import FantasyConfig
from dao.base import FantasyBaseDao
from dao.blake import BlakeRedditDao
from dao.dom import DomDao
from dao.ep import EliteProspectsDao
from dao.kkupfl_adp import KKUPFLAdpDao
from dao.kkupfl_scoring import KKUPFLScoringDao
from dao.laidlaw import SteveLaidlawDao
# from dao.nhl import NHLDao
# from dao.schedule import JeffMaiScheduleDao
from model.league import League
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


class ProjectionsController:
    def __init__(self, league: str):
        self.league = get_daos(league)
    
    
    def write_consolidated_rankings(league: str, final_rankings: dict):
        controller = ProjectionsSvc(get_daos(league))
        write_consolidated_rankings(controller, league, averaged_rankings=averaged_rankings)