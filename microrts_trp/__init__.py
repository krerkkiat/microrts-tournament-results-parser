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
        return name[: max_length + 1] + "..."
    else:
        return name


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "map_folder",
        metavar="map-folder",
        nargs="?",
        default=".",
        help="A path to the map folder containing `tournament_N` folders.",
    )
    parser.add_argument("--full", action="store_true", help="Show full win rates table.")
    parser.add_argument("--full-bot-name", action="store_true", help="Do not shorten the name of the bot.")
    parser.add_argument("--format", choices=("github", "latex"), default="github", help="A format for tabulate's table.")

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
        # Rename the bots in the index.
        win_rates.index = win_rates.index.map(shorten_bot_name)

        # Rename the bots in the column's name.
        col_names = win_rates.columns.values.tolist()
        new_col_names = {name: shorten_bot_name(name) for name in col_names}
        win_rates = win_rates.rename(columns=new_col_names)

    print(f"Map: {map_result.name}")
    print(f"Number of AIs: {map_result.win_rates.shape[0]}")
    print(
        f"Total battles / bot: {len(map_result.tournaments[0].ai_names) * map_result.total_iterations}"
    )
    print(
        tabulate(
            win_rates,
            tablefmt=args.format,
            headers=["Bot"] + win_rates.columns.tolist(),
            floatfmt=".2f",
        )
    )
