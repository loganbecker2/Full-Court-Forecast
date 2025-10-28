# -*- coding: utf-8 -*-
"""
Season stats scraper.

Returns a single DataFrame with a Season column.
"""

from __future__ import annotations

import os
import random
import time
from typing import Iterable

import pandas as pd

from .common import read_html_table, clean_season_stats


BASE_URL = "https://www.sports-reference.com/cbb"


def scrape_season_stats(seasons: Iterable[int], base_url: str = BASE_URL) -> pd.DataFrame:
    all_data = pd.DataFrame()

    for season in seasons:
        url = f"{base_url}/seasons/{season}-school-stats.html"
        print(f"Scraping season stats: {url}")
        df = read_html_table(url)
        if df is None:
            print(f"No table returned for season {season}.")
            continue

        df = clean_season_stats(df)
        df['Season'] = season
        all_data = pd.concat([all_data, df], ignore_index=True)

        # Polite delay
        time.sleep(random.randint(5, 10))

    return all_data


if __name__ == "__main__":
    # Example run that saves to DataFrames/Overall-Data
    seasons = [2022, 2023, 2024, 2025]
    out_dir = os.path.join("DataFrames", "Overall-Data")
    os.makedirs(out_dir, exist_ok=True)

    df = scrape_season_stats(seasons)
    combined_path = os.path.join(out_dir, "season_stats.csv")
    df.to_csv(combined_path, index=False)
    print(f"Saved combined season stats to {combined_path}")

    # Save per-season for convenience
    for year in df["Season"].unique():
        year_df = df[df["Season"] == year]
        # match existing naming convention like 2022_stats.csv
        year_file = os.path.join(out_dir, f"{year}_stats.csv")
        year_df.to_csv(year_file, index=False)
        print(f"Saved {year} season stats to {year_file}")

