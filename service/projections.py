import csv
import re
from pathlib import Path
from typing import Tuple

from pandas import DataFrame

from config.config import FantasyConfig
from dao.reader.base import BaseProjectionsReader
from dao.reader.nhl import NHLReader
from data.dynamic.drafted import KKUPFL_DRAFTED, PA_DRAFTED
from model.league import League
from model.season import Season
from dao.reader import (
    BlakeRedditReader, 
    DomReader, 
    EliteProspectsReader, 
    KKUPFLAdpReader, 
    KKUPFLScoringReader,
    SteveLaidlawReader
)


OUTPUT_DIR = Path(__file__).parent / "output"



#KKUPFL_READERS = [
#    BlakeRedditReader(FantasyConfig.projection_files.BLAKE_KKUPFL),
#    DomReader(FantasyConfig.projection_files.DOM_KKUPFL),
#    DomReader(FantasyConfig.projection_files.DOM_KKUPFL, rank_col='/GP', ascending=False),
#    KKUPFLScoringReader(FantasyConfig.projection_files.KKUPFL_SCORING, "202324"),
#    KKUPFLScoringReader(FantasyConfig.projection_files.KKUPFL_SCORING, "202223"),
#    KKUPFLScoringReader(FantasyConfig.projection_files.KKUPFL_SCORING, "202122"),
#]


#PUCKIN_AROUND_READERS = [
#    BlakeRedditReader(FantasyConfig.projection_files.BLAKE_PA),
#    DomReader(FantasyConfig.projection_files.DOM_PA),
#    DomReader(FantasyConfig.projection_files.DOM_PA, rank_col='/GP', ascending=False),
#]


def populate_averaged_rankings(rankings: dict):
    """{<player>: { "ranks": [R1, R2, ...], "count": len(ranks)}}"""
    for player in rankings:
        ranks = [r for r in rankings[player]['ranks']]
        total_weighted_rank = sum([x.rank * x.weight for x in ranks])
        total_weight = sum([x.weight for x in ranks])
        rankings[player]['avg_rk'] = total_weighted_rank / total_weight


def write_avg_ranks_to_csv(league: League, sorted_ranks: list):
    outfile = OUTPUT_DIR / FantasyConfig.season / f"{league}_ranks.csv"
    print(f"Writing results for {league} to {outfile}")
    with open(outfile, "w", newline="") as f:
        writer = csv.writer(f)
        for rank_info in sorted_ranks:
            name = rank_info[0]
            avg_rank = round(rank_info[1]['avg_rk'], 2)
            count = rank_info[1]['count']
            ranks = "  |".join(["  " + str(r) for r in rank_info[1]['ranks'] if r.weight > 0])
            writer.writerow([name, avg_rank, count, ranks])


#def get_projections_by_regexes(proj_controller: ProjectionsSvc, historical_controller: ProjectionsSvc, regexes: list[str]) -> dict[BaseProjectionsReader, DataFrame]:
#    matched_players = set()
#    projections_by_reader = proj_controller.get_matches_for_readers(regexes)
#    for reader, results in projections_by_reader.items():
#        projections_by_reader[reader] = proj_controller.refine_results(
#            reader,
#            results,
#            positions_rgx=positions_rgx,
#            excluded=excluded,
#            count=count)
#        matched_players.update(projections_by_reader[reader][reader.primary_col].tolist())
#
#    historical_stats_by_reader = historical_controller.get_matches_for_readers(matched_players)
#    return projections_by_reader | historical_stats_by_reader


#def write_consolidated_rankings(controller: ProjectionsSvc, league: str,
#                                averaged_rankings: dict):
#    '''
#    Generates a final consolidated and weighted average rankings list and writes it to a file.
#    '''
#    for reader in controller.readers:
#        results = controller.get_matches(reader)
#        controller.register_to_averaged_rankings(reader, results,
#                                                 averaged_rankings)
#    populate_averaged_rankings(averaged_rankings)
#    sorted_players = sorted(averaged_rankings.items(),
#                            key=lambda item: item[1]['avg_rk'])
#    write_avg_ranks_to_csv(league, sorted_players)


class ProjectionsSvc:
    def __init__(self, league: League, season: Season):
        self.league = league
        self.season = season
        base_readers = [
            KKUPFLAdpReader(FantasyConfig.projection_files.KKUPFL_ADP, self.season) if self.season in KKUPFLAdpReader.seasons else None,
            EliteProspectsReader(FantasyConfig.projection_files.ELITE_PROSPECTS, self.season) if self.season in EliteProspectsReader.seasons else None,
            SteveLaidlawReader(FantasyConfig.projection_files.STEVE_LAIDLAW, self.season) if self.season in SteveLaidlawReader.seasons else None,
            NHLReader(FantasyConfig.projection_files.NHL, self.season) if self.season in NHLReader.seasons else None,
        ]
        self.base_readers = [r for r in base_readers if r is not None]

#    @staticmethod
#    def print_results(results: DataFrame):
#        print(f"({len(results)} players)")
#        print(results.to_string(index=False))

    @staticmethod
    def get_matches(reader: BaseProjectionsReader, regexes: list[str] = ['.*']) -> DataFrame:
        matches = reader.find_by_rgxs(regexes)
        return matches

    @staticmethod
    def _trim_results(results: DataFrame, count:str):
        if count > 0:
            return results.head(count)
        return results

    @staticmethod
    def _filter_excluded_players(reader: BaseProjectionsReader, results: DataFrame, excluded: list[str]) -> DataFrame:
        if len(excluded) == 0:
            return results

        patternDel = "|".join(excluded)
        filter = results[reader.primary_col].str.contains(patternDel, flags=re.IGNORECASE, regex=True)
        return results[~filter]

    @staticmethod
    def _filter_positions(reader: BaseProjectionsReader, results: DataFrame, positions_rgx) -> DataFrame:
        if reader.position_col == 'N/A':
            print(f"{reader} reader does not support position filtering")
            return results
        filter = results[reader.position_col].str.contains(positions_rgx, flags=re.IGNORECASE, regex=True)
        return results[filter]

    def refine_results(self, reader: BaseProjectionsReader, results: DataFrame, positions_rgx: list[str], excluded: list[str] = None, count: int = -1) -> DataFrame:
        results = self._filter_positions(reader, results, positions_rgx)
        results = self._filter_excluded_players(reader, results, excluded)
        results = self._trim_results(results, count)
        return results

    @staticmethod
    def register_to_averaged_rankings(reader: BaseProjectionsReader, results: DataFrame, average_rankings: dict):
        for player_name in results[reader.primary_col]:
            reader.add_to_averaged_rankings(player_name, average_rankings)

    
    def get_readers(self) -> list[BaseProjectionsReader]:
        '''
        Gets a list of readers for the service.
        
        If the readers param is present, use it to determine which readers to use.
        If not, default to the readers associated with the given league.
        '''
        readers = self.base_readers
        import ipdb; ipdb.set_trace()
#        if self.league == League.KKUPFL:
#            self.base_readers.extend(KKUPFL_READERS)
#        elif self.league == League.PUCKIN_AROUND:
#            self.base_readers.extend(PUCKIN_AROUND_READERS)
        return readers


    def get_matches_for_readers(self, regexes: list[str]) -> dict[BaseProjectionsReader, DataFrame]:
        '''
        Searches all readers for rows matching the passed in regexes.

        Returns a dictionary which maps each reader to its corresponding result set.
        '''
        if regexes is None:
            regexes = ['.*']
        reader_results = dict()
        for reader in self.readers:
            reader_results[reader] = self.get_matches(reader, regexes=regexes)
        return reader_results

    def print_matches_for_all_readers(self, reader_results_map: dict[BaseProjectionsReader, DataFrame]) -> None:
        for reader, results in reader_results_map.items():
            reader.print(results)

    def get_top_players_for_readers(self):
        '''
        Searches all readers for rows matching the passed in regexes.

        Returns a dictionary which maps each reader to its corresponding result set.
        '''
        reader_results = dict()
        for reader in self.readers:
            reader_results[reader] = self.get_matches(reader, regexes=['.*'])
        return reader_results

    def get_rankings(regexes: list[str]) -> dict:
        pass