# -*- coding: utf-8 -*-
"""
Team gamelogs scraper.

Returns a single DataFrame with columns including Season and School.
"""

from __future__ import annotations

import os
import random
import time
from typing import Iterable

import pandas as pd

from .common import read_html_table, get_school_list, clean_gamelogs


BASE_URL = "https://www.sports-reference.com/cbb"


def scrape_team_gamelogs(seasons: Iterable[int], base_url: str = BASE_URL) -> pd.DataFrame:
    all_data = pd.DataFrame()

    for season in seasons:
        print(f"Gathering school list for {season}...")
        schools = get_school_list(season)
        for school in schools:
            url = f"{base_url}/schools/{school}/men/{season}-gamelogs.html"
            print(f"Scraping gamelog: {url}")
            df = read_html_table(url)
            if df is None:
                print(f"No table for {school}, {season}")
                continue

            df['Season'] = season
            df['School'] = school
            df = clean_gamelogs(df)
            all_data = pd.concat([all_data, df], ignore_index=True)

            # Polite delay
            time.sleep(random.randint(5, 10))

    return all_data


if __name__ == "__main__":
    # Example run that saves to DataFrames/Team-Gamelogs
    seasons = [2022, 2023, 2024, 2025]
    out_dir = os.path.join("DataFrames", "Team-Gamelogs")
    os.makedirs(out_dir, exist_ok=True)

    df = scrape_team_gamelogs(seasons)
    combined_path = os.path.join(out_dir, "all_team_gamelogs.csv")
    df.to_csv(combined_path, index=False)
    print(f"Saved combined team gamelogs to {combined_path}")

    # Save per-season and per-team
    for year in df["Season"].unique():
        year_folder = os.path.join(out_dir, str(year))
        os.makedirs(year_folder, exist_ok=True)
        year_df = df[df["Season"] == year]

        # Partition by team
        for school in sorted(year_df["School"].unique()):
            team_df = year_df[year_df["School"] == school]
            file_path = os.path.join(year_folder, f"{school}-gamelogs.csv")
            team_df.to_csv(file_path, index=False)

    print("Finished saving team gamelogs.")

