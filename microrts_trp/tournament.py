from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import functools

import numpy as np
import pandas as pd


def shorten_bot_name(name: str, max_length=35) -> str:
    if len(name) > max_length:
        return name[: max_length + 1] + "..."
    else:
        return name

@dataclass
class TournamentConfig:
    """Configuration for each run of the tournament."""

    iterations: int


@dataclass
class TournamentResult:
    """Representation of the tournament.csv file."""

    ai_names: list[str]
    maps: list[str]
    config: TournamentConfig
    wins_table: pd.DataFrame
    ties_table: pd.DataFrame

    def calculate_scores(self):
        return self.wins_table + (self.ties_table * 0.5)


@dataclass
class MapResult:
    name: str
    tournaments: list[TournamentResult]

    def __str__(self):
        return f"MapResult[name={self.name}, win_rates={self.win_rates}]"

    @functools.cached_property
    def total_iterations(self) -> int:
        total_iterations = 0
        for t in self.tournaments:
            total_iterations += t.config.iterations
        return total_iterations

    @functools.cached_property
    def final_scores(self) -> pd.DataFrame:
        final_scores = None

        for t in self.tournaments:
            if final_scores is None:
                final_scores = t.calculate_scores()
            else:
                final_scores += t.calculate_scores()
        return final_scores

    @functools.cached_property
    def win_rates(self) -> pd.DataFrame:
        win_rates_table = (self.final_scores * 100.0) / self.total_iterations

        return win_rates_table
    
    def format_win_rates_for_human(self, show_detail=False, show_full_bot_name=False) -> pd.DataFrame:
        final_scores = self.final_scores.copy()
        final_scores["Total"] = final_scores.sum(axis=1)

        win_rates = self.win_rates.copy()
        win_rates["Win Rate"] = (
            final_scores["Total"]
            * 100.0
            / (len(self.tournaments[0].ai_names) * self.total_iterations)
        )

        # Move 'Win Rate' column to the left.
        cols = win_rates.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        win_rates = win_rates.loc[:, cols]

        win_rates = win_rates.sort_values(by="Win Rate", ascending=False)

        if not show_detail:
            # Remove the detail columns.
            cols = win_rates.columns.tolist()
            win_rates = win_rates.drop(columns=cols[1:])

        if not show_full_bot_name:
            # Rename the bots in the index.
            win_rates.index = win_rates.index.map(shorten_bot_name)

            # Rename the bots in the column's name.
            col_names = win_rates.columns.values.tolist()
            new_col_names = {name: shorten_bot_name(name) for name in col_names}
            win_rates = win_rates.rename(columns=new_col_names)

        return win_rates


def parse_tournament_file(path: Path | str) -> Optional[TournamentResult]:
    if isinstance(path, str):
        path = Path(path)

    with open(path, "r") as in_f:
        try:
            lines = in_f.readlines()

            current_section: str = ""
            ai_names: list[str] = []
            maps: list[str] = []
            config = dict()
            wins_table = None
            ties_table = None
            row_count = 0
            for line in lines:
                # Capture the section change.
                if line.strip() == "AIs":
                    current_section = "ai-list"
                    continue
                elif line.strip() == "maps":
                    current_section = "map-list"
                    continue
                elif line.strip() == "Wins:":
                    current_section = "wins-table"
                    wins_table = np.zeros((len(ai_names), len(ai_names)))
                    row_count = 0
                    continue
                elif line.strip() == "Ties:":
                    current_section = "ties-table"
                    ties_table = np.zeros((len(ai_names), len(ai_names)))
                    row_count = 0
                    continue
                elif line.strip() == "Average Game Length:":
                    current_section = "avg-game-length-table"
                    continue

                tokens = line.split("\t")
                if len(tokens) > 1 and tokens[0] == "iterations":
                    config["iterations"] = int(tokens[1])

                if current_section == "map-list":
                    maps.append(line.strip())
                elif current_section == "ai-list":
                    ai_names.append(line.strip())
                elif current_section == "wins-table":
                    tokens = [
                        int(t)
                        for t in line.strip().split("\t")
                        if len(t.strip()) != 0
                    ]
                    wins_table[row_count, :] = tokens
                    row_count += 1
                elif current_section == "ties-table":
                    tokens = [
                        int(t)
                        for t in line.strip().split("\t")
                        if len(t.strip()) != 0
                    ]
                    ties_table[row_count, :] = tokens
                    row_count += 1

            return TournamentResult(
                ai_names,
                maps,
                TournamentConfig(**config),
                pd.DataFrame(data=wins_table, columns=ai_names, index=ai_names),
                pd.DataFrame(data=ties_table, columns=ai_names, index=ai_names),
            )
        except Exception:
            return None


def parse_map_folder(path: Path | str) -> MapResult:
    if isinstance(path, str):
        path = Path(path)

    path = path.absolute()

    if not path.exists():
        raise RuntimeError(f"path '{str(path)}' does not exist")
    
    map_name = "tournament.csv"
    if path.name == "tournament.csv":
        raw_tournament_files = [path]
        tournaments = [parse_tournament_file(f) for f in raw_tournament_files]
        if len(tournaments) != 0 and tournaments[0] is not None:
            map_name = tournaments[0].maps[0]

    elif path.is_dir():
        map_name = path.name
        raw_tournament_files = list(path.glob("*/tournament.csv"))
        tournaments = [parse_tournament_file(f) for f in raw_tournament_files]
    else:
        raise RuntimeError(f"path '{str(path)}' is not a folder and it is not the 'tournament.csv' file itself.")

    map_result = MapResult(name=map_name, tournaments=tournaments)
    return map_result
