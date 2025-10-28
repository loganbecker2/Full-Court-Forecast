# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 15:47:30 2025

@author: Logmo
"""

import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
#%% Import csv files
# Root folders for saved CSVs
OVERALL_DIR = os.path.join("DataFrames", "Overall-Data")
GAMELOGS_DIR = os.path.join("DataFrames", "Team-Gamelogs")
def load_season_stats(overall_dir: str = OVERALL_DIR) -> pd.DataFrame:
    """Load season stats CSVs from DataFrames/Overall-Data.
    Tries the combined file first (season_stats.csv). If missing, it
    concatenates any "*_stats.csv" files present in the folder.
    """
    combined_path = os.path.join(overall_dir, "season_stats.csv")
    if os.path.isfile(combined_path):
        return pd.read_csv(combined_path)
    # Fallback: combine any per-season files like 2022_stats.csv, etc.
    frames = []
    try:
        for name in os.listdir(overall_dir):
            if name.endswith("_stats.csv") and name != "season_stats.csv":
                frames.append(pd.read_csv(os.path.join(overall_dir, name)))
    except FileNotFoundError:
        pass
    if frames:
        return pd.concat(frames, ignore_index=True)
    raise FileNotFoundError(
        f"No season stats CSVs found in {overall_dir}. "
        "Expected 'season_stats.csv' or files like '2022_stats.csv'."
    )
def load_team_gamelogs(gamelogs_dir: str = GAMELOGS_DIR) -> pd.DataFrame:
    """Load team gamelog CSVs from DataFrames/Team-Gamelogs.
    Supports two layouts:
    - Combined file (if you created one elsewhere), e.g. all_team_gamelogs.csv
    - Per-season subfolders (e.g., 2022/, 2023/, ...), each containing
      many "<school>-gamelogs.csv" files. Adds a Season column from folder name
      if not present in the CSV.
    """
    # Try a single combined file first if it exists
    combined_path = os.path.join(gamelogs_dir, "all_team_gamelogs.csv")
    if os.path.isfile(combined_path):
        return pd.read_csv(combined_path)
    # Otherwise, walk each season subfolder and combine per-team logs
    all_frames = []
    if not os.path.isdir(gamelogs_dir):
        raise FileNotFoundError(f"Gamelogs directory not found: {gamelogs_dir}")
    for entry in sorted(os.listdir(gamelogs_dir)):
        season_path = os.path.join(gamelogs_dir, entry)
        if not os.path.isdir(season_path):
            continue
        season = entry  # folder name (e.g., '2022')
        for fname in os.listdir(season_path):
            if not fname.endswith("-gamelogs.csv"):
                continue
            fpath = os.path.join(season_path, fname)
            df = pd.read_csv(fpath)
            # Ensure Season column exists; if not, add from folder name
            if "Season" not in df.columns:
                df["Season"] = season
            # Ensure School column exists; if not, derive from filename
            if "School" not in df.columns:
                school_slug = fname.replace("-gamelogs.csv", "")
                df["School"] = school_slug
            all_frames.append(df)
    if not all_frames:
        raise FileNotFoundError(
            f"No team gamelog CSVs found under {gamelogs_dir}. "
            "Expected 'all_team_gamelogs.csv' or per-season folders with CSVs."
        )
    return pd.concat(all_frames, ignore_index=True)

season_stats_df = load_season_stats()
team_gamelogs_df = load_team_gamelogs()
print(season_stats_df.shape, team_gamelogs_df.shape)