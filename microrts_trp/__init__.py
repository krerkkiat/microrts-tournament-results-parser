"""
Analyze tournament results.

Implement the same calculation as the official tournament result analysis.
"""

__version__ = "0.1.1"

import click
import pandas as pd
from tabulate import tabulate

from microrts_trp.tournament import parse_map_folder


def shorten_bot_name(name: str, max_length=35) -> str:
    if len(name) > max_length:
        return name[: max_length + 1] + "..."
    else:
        return name


@click.group()
def cli():
    pass


@cli.command(short_help="Show this message.")
@click.pass_context
def help(ctx):
    click.echo(cli.get_help(ctx))


@cli.command(name="view", short_help="Parse a map-folder and show the win rates table.")
@click.argument("map_folder")
@click.option(
    "--detail/--no-detail",
    show_default=True,
    default=False,
    help="Show the detailed win rates table or show only the win rates.",
)
@click.option("--full-bot-name", help="Do not shorten the name of the bot.")
@click.option(
    "--format",
    type=click.Choice(["github", "latex"]),
    show_default=True,
    default="github",
    help="Do not shorten the name of the bot.",
)
def view_map_folder_command(map_folder, detail, full_bot_name, format):
    map_result = parse_map_folder(map_folder)
    win_rates = map_result.format_win_rates_for_human(detail, full_bot_name)

    print(f"Map: {map_result.name}")
    print(f"Number of AIs: {map_result.win_rates.shape[0]}")
    print(
        f"Total battles / bot: {len(map_result.tournaments[0].ai_names) * map_result.total_iterations}"
    )
    print(
        tabulate(
            win_rates,
            tablefmt=format,
            headers=["Bot"] + win_rates.columns.tolist(),
            floatfmt=".2f",
        )
    )


@cli.command(name="compare", short_help="Compare win rates of two map folders.")
@click.argument("map_folder_1")
@click.argument("map_folder_2")
@click.option("--full-bot-name", help="Do not shorten the name of the bot.")
@click.option(
    "--format",
    type=click.Choice(["github", "latex"]),
    show_default=True,
    default="github",
    help="Do not shorten the name of the bot.",
)
def compare_map_folders_command(map_folder_1, map_folder_2, full_bot_name, format):
    map_result_1 = parse_map_folder(map_folder_1)
    map_result_2 = parse_map_folder(map_folder_2)

    # Sanity checks.

    win_rates_1 = map_result_1.format_win_rates_for_human(
        show_detail=False, show_full_bot_name=full_bot_name
    )
    win_rates_2 = map_result_2.format_win_rates_for_human(
        show_detail=False, show_full_bot_name=full_bot_name
    )

    df = pd.DataFrame()
    df[map_result_1.name] = win_rates_1["Win Rate"]
    df[map_result_2.name] = win_rates_2["Win Rate"]
    changes = df[map_result_2.name] - df[map_result_1.name]
    df["Change (%)"] = (changes / df[map_result_1.name]) * 100.0
    df = df.sort_values(by="Change (%)", ascending=False)

    print(
        tabulate(
            df,
            tablefmt=format,
            headers=["Bot"] + df.columns.tolist(),
            floatfmt=".2f",
        )
    )


@cli.command(
    name="focus",
    short_help="Show focused result of one bot. How well it performs against the other bots \
                and how well the other bot perform against it.",
)
@click.argument("map_folder")
@click.argument("bot_name")
@click.option("--full-bot-name", help="Do not shorten the name of the bot.")
@click.option(
    "--format",
    type=click.Choice(["github", "latex"]),
    show_default=True,
    default="github",
    help="Do not shorten the name of the bot.",
)
def focus_command(map_folder, bot_name, full_bot_name, format):
    map_result = parse_map_folder(map_folder)

    target_bot_vs_other = pd.DataFrame()
    target_bot_vs_other[bot_name] = map_result.win_rates.loc[bot_name].transpose()
    # Remove itself from the table.
    target_bot_vs_other = target_bot_vs_other.drop(bot_name)
    target_bot_vs_other = target_bot_vs_other.sort_values(by=bot_name, ascending=False)


    print(f"Map: {map_result.name}")
    print(f"Number of AIs: {map_result.win_rates.shape[0]}")
    print(f"Bot of Interest: {bot_name}")
    print(f"\nHow well {bot_name} performed against the other bots:")
    print(
        tabulate(
            target_bot_vs_other,
            tablefmt=format,
            headers=[bot_name],
            floatfmt=".2f",
        )
    )

    other_vs_target_bot = pd.DataFrame()
    other_vs_target_bot[bot_name] = map_result.win_rates[bot_name]
    other_vs_target_bot = other_vs_target_bot.drop(bot_name)
    other_vs_target_bot = other_vs_target_bot.sort_values(by=bot_name, ascending=False)
    print(f"\nHow well the other bots performed against {bot_name}:")
    print(
        tabulate(
            other_vs_target_bot,
            tablefmt=format,
            headers=["Other bots", bot_name],
            floatfmt=".2f",
        )
    )

@cli.command(
    name="focus-compare",
    short_help="Show focused result of one bot. How well it performs against the other bots \
                and how well the other bot perform against it.",
)
@click.argument("map_folder_1")
@click.argument("map_folder_2")
@click.argument("bot_name")
@click.option("--full-bot-name", help="Do not shorten the name of the bot.")
@click.option(
    "--format",
    type=click.Choice(["github", "latex"]),
    show_default=True,
    default="github",
    help="Do not shorten the name of the bot.",
)
def focus_compare_command(map_folder_1, map_folder_2, bot_name, full_bot_name, format):
    map_result_1 = parse_map_folder(map_folder_1)
    map_result_2 = parse_map_folder(map_folder_2)

    target_bot_vs_other = pd.DataFrame()
    target_bot_vs_other[map_result_1.name] = map_result_1.win_rates.loc[bot_name].transpose()
    target_bot_vs_other[map_result_2.name] = map_result_2.win_rates.loc[bot_name].transpose()
    # Remove itself from the table.
    target_bot_vs_other = target_bot_vs_other.drop(bot_name)
    target_bot_vs_other = target_bot_vs_other.sort_values(by=map_result_2.name, ascending=False)

    print(f"Bot of Interest: {bot_name}")
    print(f"\nHow well {bot_name} performed against the other bots:")
    print(
        tabulate(
            target_bot_vs_other,
            tablefmt=format,
            headers=[map_result_1.name, map_result_2.name],
            floatfmt=".2f",
        )
    )

    other_vs_target_bot = pd.DataFrame()
    other_vs_target_bot[map_result_1.name] = map_result_1.win_rates[bot_name]
    other_vs_target_bot[map_result_2.name] = map_result_2.win_rates[bot_name]
    other_vs_target_bot = other_vs_target_bot.drop(bot_name)
    other_vs_target_bot = other_vs_target_bot.sort_values(by=map_result_2.name, ascending=False)
    print(f"\nHow well the other bots performed against {bot_name}:")
    print(
        tabulate(
            other_vs_target_bot,
            tablefmt=format,
            headers=["Other bots", map_result_1.name, map_result_2.name],
            floatfmt=".2f",
        )
    )