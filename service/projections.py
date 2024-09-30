import csv
import re
from pathlib import Path
from telnetlib import DO
from typing import Tuple, Union

from pandas import DataFrame

from config.config import FantasyConfig as FC
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


def populate_averaged_rankings(rankings: dict):
    """{<player>: { "ranks": [R1, R2, ...], "count": len(ranks)}}"""
    for player in rankings:
        ranks = [r for r in rankings[player]['ranks']]
        total_weighted_rank = sum([x.rank * x.weight for x in ranks])
        total_weight = sum([x.weight for x in ranks])
        rankings[player]['avg_rk'] = total_weighted_rank / total_weight


def write_avg_ranks_to_csv(league: League, sorted_ranks: list):
    outfile = OUTPUT_DIR / FC.season / f"{league}_ranks.csv"
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

        maybe_base_readers = [
            self.maybe_load_reader(KKUPFLAdpReader, FC.projection_files.KKUPFL_ADP),
            self.maybe_load_reader(EliteProspectsReader, FC.projection_files.ELITE_PROSPECTS),
            self.maybe_load_reader(SteveLaidlawReader, FC.projection_files.STEVE_LAIDLAW),
            self.maybe_load_reader(NHLReader, FC.projection_files.NHL),
        ]

        # TODO: way to use enum directly as keys instead of using value?
        maybe_readers_by_league = {
            League.KKUPFL.value: [
                self.maybe_load_reader(BlakeRedditReader, FC.projection_files.BLAKE_KKUPFL),
                self.maybe_load_reader(DomReader, FC.projection_files.DOM_KKUPFL),
                self.maybe_load_reader(DomReader, FC.projection_files.DOM_KKUPFL, rank_col='/GP', ascending=False),
                self.maybe_load_reader(KKUPFLScoringReader, FC.projection_files.KKUPFL_SCORING, sheet_name="202324"),
                self.maybe_load_reader(KKUPFLScoringReader, FC.projection_files.KKUPFL_SCORING, sheet_name="202223"),
                self.maybe_load_reader(KKUPFLScoringReader, FC.projection_files.KKUPFL_SCORING, sheet_name="202122"),
            ],
            League.PUCKIN_AROUND.value: [
                self.maybe_load_reader(BlakeRedditReader, FC.projection_files.BLAKE_PA),
                self.maybe_load_reader(DomReader, FC.projection_files.DOM_PA),
                self.maybe_load_reader(DomReader, FC.projection_files.DOM_PA, rank_col='/GP', ascending=False),
            ]
        }
        self.readers = [r for r in maybe_base_readers + maybe_readers_by_league[self.league.value] if r is not None]


    def maybe_load_reader(self, reader: BaseProjectionsReader, filename: str, **kwargs) -> Union[None, BaseProjectionsReader]:
        '''Conditionally instantiates passed in BaseProjectionReader if it supports the current season'''
        return reader(filename, self.season, **kwargs) if self.season in reader.seasons else None

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
