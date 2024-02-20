"""
Analyze tournament results.

Implement the same calculation as the official tournament result analysis.
"""

__version__ = "0.0.1"

from tabulate import tabulate

from microrts_trp.tournament import (
    parse_map_folder,
)

def shorten_bot_name(name: str, max_length=35) -> str:
    if len(name) > max_length:
        return name[:max_length+1] + "..."
    else:
        return name


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("map_folder", metavar="map-folder", nargs="?", default=".")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--full-bot-name", action="store_true")

    args = parser.parse_args()
    map_result = parse_map_folder(args.map_folder)

    final_scores = map_result.final_scores.copy()
    final_scores["Total"] = final_scores.sum(axis=1)

    win_rates = map_result.win_rates.copy()
    win_rates["Win Rate"] = (
        final_scores["Total"]
        * 100.0
        / (len(map_result.tournaments[0].ai_names) * map_result.total_iterations)
    )
    # Move 'Win Rate' column to the left.
    cols = win_rates.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    win_rates = win_rates.loc[:, cols]

    win_rates = win_rates.sort_values(by="Win Rate", ascending=False)

    if not args.full:
        # Remove the detail columns.
        cols = win_rates.columns.tolist()
        win_rates = win_rates.drop(columns=cols[1:])

    if not args.full_bot_name:
        win_rates.index = win_rates.index.map(shorten_bot_name)

    print(f"Map: {map_result.name}")
    print(f"Number of AIs: {map_result.win_rates.shape[0]}")
    print(f"Total battles / bot: {len(map_result.tournaments[0].ai_names) * map_result.total_iterations}")
    print(
        tabulate(
            win_rates,
            tablefmt="github",
            headers=["Bot"] + win_rates.columns.tolist(),
            floatfmt=".2f",
        )
    )
