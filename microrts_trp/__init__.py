"""
Analyze tournament results.

Implement the same calculation as the official tournament result analysis.
"""

__version__ = "0.0.1"

from tabulate import tabulate

from microrts_trp.tournament import (
    parse_map_folder,
)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("map_folder", metavar="map-folder", nargs="?", default=".")

    args = parser.parse_args()
    map_result = parse_map_folder(args.map_folder)

    final_scores = map_result.final_scores.copy()
    final_scores["Total"] = final_scores.sum(axis=1)

    win_rates = map_result.win_rates.copy()
    win_rates["Total"] = (
        final_scores["Total"]
        * 100.0
        / (len(map_result.tournaments[0].ai_names) * map_result.total_iterations)
    )
    # Move Total column to the left
    cols = win_rates.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    win_rates = win_rates.loc[:, cols]

    print(f"\nMap: {map_result.name}")
    print(
        tabulate(
            win_rates.sort_values(by="Total", ascending=False),
            tablefmt="github",
            headers=["Bot"] + win_rates.columns.to_list(),
            floatfmt=".2f",
        )
    )
