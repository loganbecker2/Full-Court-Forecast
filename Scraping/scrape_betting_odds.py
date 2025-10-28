# -*- coding: utf-8 -*-
# --- UNFINISHED ---

"""
Betting odds scraper (stub).

Implement vendor-specific fetching here. For now, returns an empty DataFrame
to allow the orchestrator to skip saving when no data is provided.
"""

from __future__ import annotations

import pandas as pd


def scrape_betting_odds(*args, **kwargs) -> pd.DataFrame:
    """Placeholder implementation.

    Replace with logic to fetch and normalize odds. Expected columns might
    include: Date, Book, Team, Opponent, Open, Close, Line, Total, etc.
    """
    return pd.DataFrame()


if __name__ == "__main__":
    df = scrape_betting_odds()
    print("Betting odds rows:", len(df))

