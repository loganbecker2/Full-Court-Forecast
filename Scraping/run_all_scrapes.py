# -*- coding: utf-8 -*-
"""
Run all scrapers and save outputs under DataFrames/.

This orchestrator keeps scrapers pure (return DataFrames) and centralizes
saving, partitioning, and simple logging.
"""

from __future__ import annotations

import argparse
import os
from typing import Iterable

import pandas as pd

from .scrape_season_stats import scrape_season_stats, BASE_URL as BASE_URL_SEASON
from .scrape_team_gamelogs import scrape_team_gamelogs, BASE_URL as BASE_URL_GAMELOGS
from .scrape_betting_odds import scrape_betting_odds


def save_season_stats(df: pd.DataFrame, out_root: str) -> None:
    out_dir = os.path.join(out_root, "Overall-Data")
    os.makedirs(out_dir, exist_ok=True)
    combined_path = os.path.join(out_dir, "season_stats.csv")
    df.to_csv(combined_path, index=False)
    print(f"Saved combined season stats to {combined_path}")

    for year in df["Season"].unique():
        year_df = df[df["Season"] == year]
        year_file = os.path.join(out_dir, f"{year}_stats.csv")
        year_df.to_csv(year_file, index=False)
        print(f"Saved {year} season stats to {year_file}")


def save_team_gamelogs(df: pd.DataFrame, out_root: str) -> None:
    out_dir = os.path.join(out_root, "Team-Gamelogs")
    os.makedirs(out_dir, exist_ok=True)

    combined_path = os.path.join(out_dir, "all_team_gamelogs.csv")
    df.to_csv(combined_path, index=False)
    print(f"Saved combined team gamelogs to {combined_path}")

    for year in df["Season"].unique():
        year_folder = os.path.join(out_dir, str(year))
        os.makedirs(year_folder, exist_ok=True)
        year_df = df[df["Season"] == year]
        for school in sorted(year_df["School"].unique()):
            team_df = year_df[year_df["School"] == school]
            file_path = os.path.join(year_folder, f"{school}-gamelogs.csv")
            team_df.to_csv(file_path, index=False)


def run(seasons: Iterable[int], out_root: str = "DataFrames", seasons_only=False, gamelogs_only=False, odds=False) -> None:
    if not gamelogs_only:
        season_df = scrape_season_stats(seasons, base_url=BASE_URL_SEASON)
        if not season_df.empty:
            save_season_stats(season_df, out_root)
        else:
            print("Season stats scraper returned no rows; skipping save.")

    if not seasons_only:
        glogs_df = scrape_team_gamelogs(seasons, base_url=BASE_URL_GAMELOGS)
        if not glogs_df.empty:
            save_team_gamelogs(glogs_df, out_root)
        else:
            print("Team gamelogs scraper returned no rows; skipping save.")

    if odds:
        odds_df = scrape_betting_odds()
        if odds_df is None or odds_df.empty:
            print("Betting odds scraper returned no rows; skipping save.")
        else:
            odds_dir = os.path.join(out_root, "Betting-Odds")
            os.makedirs(odds_dir, exist_ok=True)
            # Caller should decide partitioning; here we just drop a snapshot
            snapshot_path = os.path.join(odds_dir, "odds_snapshot.csv")
            odds_df.to_csv(snapshot_path, index=False)
            print(f"Saved odds snapshot to {snapshot_path}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run CBB scrapers and save CSVs")
    p.add_argument("--start", type=int, default=2022, help="start season year")
    p.add_argument("--end", type=int, default=2025, help="end season year (inclusive)")
    p.add_argument("--out", type=str, default="DataFrames", help="output root directory")
    p.add_argument("--seasons-only", action="store_true", help="scrape only season stats")
    p.add_argument("--gamelogs-only", action="store_true", help="scrape only team gamelogs")
    p.add_argument("--odds", action="store_true", help="also run betting odds scraper (if implemented)")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    seasons = list(range(args.start, args.end + 1))
    run(
        seasons=seasons,
        out_root=args.out,
        seasons_only=args.seasons_only,
        gamelogs_only=args.gamelogs_only,
        odds=args.odds,
    )

