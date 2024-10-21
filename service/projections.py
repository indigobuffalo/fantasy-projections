from calendar import day_abbr
import csv
import re
from pathlib import Path
from telnetlib import DO
from typing import Tuple, Union

import pandas as pd
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

        maybe_readers_by_league = {
            League.KKUPFL: [
                self.maybe_load_reader(BlakeRedditReader, FC.projection_files.BLAKE_KKUPFL),
                self.maybe_load_reader(DomReader, FC.projection_files.DOM_KKUPFL),
                self.maybe_load_reader(DomReader, FC.projection_files.DOM_KKUPFL, rank_col='/GP', ascending=False),
                self.maybe_load_reader(KKUPFLScoringReader, FC.projection_files.KKUPFL_SCORING, sheet_name="202324"),
                self.maybe_load_reader(KKUPFLScoringReader, FC.projection_files.KKUPFL_SCORING, sheet_name="202223"),
                self.maybe_load_reader(KKUPFLScoringReader, FC.projection_files.KKUPFL_SCORING, sheet_name="202122"),
            ],
            League.PUCKIN_AROUND: [
                self.maybe_load_reader(BlakeRedditReader, FC.projection_files.BLAKE_PA),
                self.maybe_load_reader(DomReader, FC.projection_files.DOM_PA),
                self.maybe_load_reader(DomReader, FC.projection_files.DOM_PA, rank_col='/GP', ascending=False),
            ]
        }

        self.readers = [r for r in maybe_base_readers + maybe_readers_by_league[self.league] if r is not None]


    def maybe_load_reader(self, reader: BaseProjectionsReader, filename: str, **kwargs) -> Union[None, BaseProjectionsReader]:
        '''Conditionally instantiates passed in BaseProjectionReader if it supports the current season'''
        return reader(filename, self.season, **kwargs) if self.season in reader.seasons else None

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
        """Searches all readers for rows matching the passed in regexes.

        Returns:
            dict: maps each reader to its corresponding result set
        """
        reader_results = dict()
        for reader in self.readers:
            reader_results[reader] = self.get_matches(reader, regexes=['.*'])
        return reader_results

    @staticmethod
    def _filter_by_primary_regex(reader: BaseProjectionsReader, df: DataFrame, rgx: str = None) -> DataFrame:
        """Filter out any undesired rows from the DataFrame using the passed regex

        Args:
            reader (BaseProjectionsReader):  The reader used to generate the matching set of rows in df.
            df (DataFrame): Dataframe containing matching reader rows.
            rgx (str): The primary column (e.g. player name) regex to use to filter out rows from df.

        Returns:
            DataFrame: A filtered set of matching rows.
        """
        if rgx is None:
            return df
        return df.loc[~df[reader.primary_col].str.contains(rgx, na=False, case=False)]

    @staticmethod
    def _filter_by_pos(reader: BaseProjectionsReader, df: DataFrame, rgx: str = None) -> DataFrame:
        """Filter out any undesired rows from the DataFrame using the passed regex

        Args:
            reader (BaseProjectionsReader):  The reader used to generate the matching set of rows in df.
            df (DataFrame): Dataframe containing matching reader rows.
            rgx (str): The positions regex to use to filter out rows from df.  Only rows matching this regex will remain.

        Returns:
            DataFrame: A set or rows whose position column matches the passed regex.
        """
        if rgx is None or reader.position_col is None:
            return df
        return df.loc[df[reader.position_col].str.contains(rgx, na=False, case=False)]

    def _filter_results(self, reader: BaseProjectionsReader, matches: DataFrame, primary_filter_rgx: str, pos_rgx: str = None) -> DataFrame:
        """Whittle down the results returned by DAO.

        Args:
            reader (BaseProjectionsReader): The reader associated with the result set
            matches (DataFrame): DataFrame holding the currently matched rows.
            primary_filter_rgx (str): Regex used to match against the primary column.
            pos_rgx (str, optional): Regex used to match against the position column.  Defaults to None.

        Returns:
            DataFrame: A whittled down dataframe that has had the desired filters applied to it.
        """
        filtered_by_primary = self._filter_by_primary_regex(reader, matches, primary_filter_rgx)
        filtered_by_pos = self._filter_by_pos(reader, filtered_by_primary, pos_rgx)
        return filtered_by_pos

    def get_rankings_per_reader(self, primary_query: str, position_query: str, primary_filter: str, limit: int = -1) -> dict[str, DataFrame]:
        """Loop through this Service's readers and formulate a list of all matching rows by reader.

        Args:
            primary_query(list[str]): Regexes used to match against the primary field (e.g. player or team name).
            primary_filter(list[str], optional): Regexes used to filter out matches. Defaults to None.
            position_query(list[str], optional): Regexes used to match against the position column. Defaults to None.
            limit (int, optional): The number of matching rows to include. Defaults to -1.

        Returns:
            dict[str, DataFrame]: A map of readers to matching rows.
        """
        results: dict[str, DataFrame] = dict()
        for reader in self.readers:
            matches = reader.query_primary_col(query=primary_query)
            filtered = self._filter_results(reader, matches, primary_filter, position_query)
            results[str(reader)] = filtered.round(decimals=1).sort_values(by=[reader.rank_col], ascending=reader.ascending).head(limit)
        return results

    @staticmethod
    def get_average_rankings(rankings: dict[str, DataFrame]) -> dict[str, DataFrame]:
        """Generates a weighted average list of rankings using all of the ranking sets in the passed dict.

        Args:
            rankings (dict[str, DataFrame]): A map of readers to rankings.

        Returns:
            dict[str, DataFrame]: _description_
        """
        pass

    def get_rankings(
        self,
        primary_query_rgxs: list[str],
        primary_filter_rgxs: list[str] = None,
        position_query_rgxs: list[str] = None,
        include_avg: bool = True,
        limit: int = -1
    ) -> dict[str, DataFrame]:
        """Gets a list of results for each reader that matches the passed
        queries and exludes results matching the passed filters.

        Args:
            primary_query_rgxs (list[str]): Regexes used to match against the primary field (e.g. player or team name).
            primary_filter_rgxs (list[str], optional): Regexes used to filter out matches. Defaults to None.
            position_query_rgxs (list[str], optional): Regexes used to match against the position column. Defaults to None.
            limit (int, optional): The number of matching rows to include. Defaults to -1.

        Returns:
            dict[str, DataFrame]: a map of readers to matching rows.  Optionally will also include a weighted average of the rankings.
        """
        results: dict[str, DataFrame] = dict()
        primary_query_rgx = "|".join(primary_query_rgxs)
        position_query_rgx = "|".join(position_query_rgxs) if position_query_rgxs is not None else None
        primary_filter_rgx = "|".join(primary_filter_rgxs) if primary_filter_rgxs is not None else None
        results.update(self.get_rankings_per_reader(primary_query_rgx, position_query_rgx, primary_filter_rgx, limit))
        if include_avg:
            results.update(self.get_average_rankings(results))
        return results
