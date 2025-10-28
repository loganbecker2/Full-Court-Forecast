# -*- coding: utf-8 -*-
"""
Common helpers for CBB scraping.

Includes:
- read_html_table: safe wrapper around pandas.read_html returning first table
- format_school_name: normalizes school names for SR URLs
- get_school_list: fetches list of schools for a season
- clean_season_stats, clean_gamelogs: dataframe cleaners reused by scrapers
"""

from __future__ import annotations

import random
import time
from typing import Optional

import pandas as pd


def read_html_table(url: str, header=(1,)) -> Optional[pd.DataFrame]:
    """Fetch first HTML table at URL with a header row.

    Returns None on error.
    """
    try:
        dfs = pd.read_html(url, header=list(header))
        if not dfs:
            return None
        return dfs[0]
    except Exception:
        return None


def format_school_name(school: str) -> str:
    school = school.lower()
    # Past seasons have ncaa in them for some teams
    school = school.replace('\xa0ncaa', '')
    school = school.replace('(', '')
    school = school.replace(')', '')
    school = school.replace('&', '')
    school = school.replace("'", "")
    school = school.replace('.', '')

    # Random school changes in their url
    school = school.replace('bowling green', 'bowling-green-state')
    school = school.replace('east texas am', 'texas-am-commerce')
    school = school.replace('fdu', 'fairleigh-dickinson')
    school = school.replace('houston christian', 'houston-baptist')
    school = school.replace('iu indy', 'iupui')
    school = school.replace('kansas city', 'missouri-kansas-city')
    school = school.replace('little rock', 'arkansas little-rock')
    if school == 'louisiana':
        school = school.replace('louisiana', 'louisiana-lafayette')
    school = school.replace('nc state', 'north-carolina-state')
    school = school.replace('omaha', 'nebraska-omaha')
    school = school.replace('purdue fort wayne', 'ipfw')
    school = school.replace('sam houston', 'sam-houston-state')
    school = school.replace('siu edwardsville', 'southern-illinois-edwardsville')
    school = school.replace('st thomas', 'st-thomas-mn')
    school = school.replace('tcu', 'texas-christian')
    school = school.replace('texas-rio grande valley', 'texas-pan-american')
    school = school.replace('the citadel', 'citadel')
    school = school.replace('uab', 'alabama-birmingham')
    school = school.replace('uc davis', 'california-davis')
    school = school.replace('uc irvine', 'california-irvine')
    school = school.replace('uc riverside', 'california-riverside')
    school = school.replace('uc san diego', 'california-san-diego')
    school = school.replace('uc santa barbara', 'california-santa-barbara')
    school = school.replace('ucf', 'central-florida')
    school = school.replace('unc asheville', 'north-carolina-asheville')
    school = school.replace('unc greensboro', 'north-carolina-greensboro')
    school = school.replace('unc wilmington', 'north-carolina-wilmington')
    school = school.replace('ut arlington', 'texas-arlington')
    school = school.replace('utah tech', 'dixie-state')
    school = school.replace('utep', 'texas-el-paso')
    school = school.replace('utsa', 'texas-san-antonio')
    school = school.replace('vmi', 'virginia-military-institute')
    school = school.replace('william  mary', 'william-mary')
    school = school.replace(' ', '-')

    return school


def get_school_list(season: int) -> list[str]:
    url = f'https://www.sports-reference.com/cbb/seasons/men/{season}-school-stats.html'
    tables = pd.read_html(url, header=[1])
    schools_df = (tables[0][tables[0].columns[1]]).dropna()
    school_list = schools_df.tolist()
    school_list = [format_school_name(school) for school in school_list]
    # Remove 'school' header row
    school_list = [school for school in school_list if school.lower() != 'school']
    time.sleep(random.randint(3, 6))
    return school_list


def clean_season_stats(df: pd.DataFrame) -> pd.DataFrame:
    df = df.loc[:, ~df.columns.str.startswith('Unnamed')]
    df = df.rename(columns={
        'W': 'W_Tot',
        'L': 'L_Tot',
        'W.1': 'W_Conf',
        'L.1': 'L_Conf',
        'W.2': 'W_Home',
        'L.2': 'L_Home',
        'W.3': 'W_Away',
        'L.3': 'L_Away',
        'Tm.': 'Tm_Pts',
        'Opp.': 'Opp_Pts',
        'SRS': 'Simple_Rating_System',
        'SOS': 'Strength_Of_Schedule',
        'W-L%': 'W_L_Percentage',
        'FG%': 'FG_Percentage',
        '3P': 'ThreeP',
        '3PA': 'ThreePA',
        '3P%': 'ThreeP_Percentage',
        'FT%': 'FT_Percentage'
    })
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)
    if 'Rk' in df.columns:
        df = df.drop('Rk', axis=1)
    if 'School' in df.columns:
        df = df.dropna(subset=['School'])
        df = df[df['School'] != 'School']
    return df


def clean_gamelogs(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df
    # delete index columns
    if 'Unnamed: 0' in df:
        df = df.drop('Unnamed: 0', axis=1)
    if 'Rk' in df:
        df = df.drop('Rk', axis=1)
    if 'Gtm' in df:
        df = df.drop('Gtm', axis=1)
    # Delete date column if not needed (keep if you want dates)
    # if 'Date' in df:
    #     df = df.drop('Date', axis=1)

    # rename columns
    df = df.rename(columns={
        'Unnamed: 3': 'Location', 'Rslt': 'Result', 'Tm': 'TeamPts', 'Opp.1': 'AwayPts',
        # Team stats
        'FG': 'Team_FG', 'FGA': 'Team_FGA', 'FG%': 'Team_FG_Percentage',
        '3P': 'Team_ThreeP', '3PA': 'Team_ThreePA', '3P%': 'Team_ThreeP_Percentage',
        '2P': 'Team_TwoP', '2PA': 'Team_TwoPA', '2P%': 'Team_TwoP_Percentage',
        'eFG%': 'Team_eFG_Percentage', 'FT': 'Team_FT', 'FTA': 'Team_FTA',
        'FT%': 'Team_FT_Percentage', 'ORB': 'Team_ORB', 'DRB': 'Team_DRB',
        'TRB': 'Team_TRB', 'AST': 'Team_AST', 'STL': 'Team_STL', 'BLK': 'Team_BLK',
        'TOV': 'Team_TOV', 'PF': 'Team_PF',
        # Opponent stats
        'FG.1': 'Away_FG', 'FGA.1': 'Away_FGA', 'FG%.1': 'Away_FG_Percentage',
        '3P.1': 'Away_ThreeP', '3PA.1': 'Away_ThreePA', '3P%.1': 'Away_ThreeP_Percentage',
        '2P.1': 'Away_TwoP', '2PA.1': 'Away_TwoPA', '2P%.1': 'Away_TwoP_Percentage',
        'eFG%.1': 'Away_eFG_Percentage', 'FT.1': 'Away_FT', 'FTA.1': 'Away_FTA',
        'FT%.1': 'Away_FT_Percentage', 'ORB.1': 'Away_ORB', 'DRB.1': 'Away_DRB',
        'TRB.1': 'Away_TRB', 'AST.1': 'Away_AST', 'STL.1': 'Away_STL',
        'BLK.1': 'Away_BLK', 'TOV.1': 'Away_TOV', 'PF.1': 'Away_PF'
    })

    # normalize values
    if 'Location' in df.columns:
        df['Location'] = df['Location'].fillna('Home')
        df.loc[df['Location'].astype(str).str.contains('@', na=False), 'Location'] = 'Away'
        df.loc[df['Location'].astype(str).str.contains('N', na=False), 'Location'] = 'Neutral'

    if 'Type' in df.columns:
        df.loc[df['Type'].astype(str).str.contains('REG (Conf)', na=False, regex=False), 'Type'] = 'Conference'
        df.loc[df['Type'].astype(str).str.contains('REG (Non-Conf)', na=False, regex=False), 'Type'] = 'Non-Conference'

    if 'OT' in df.columns:
        if df['OT'].isnull().all():
            df['OT'] = 0
        else:
            df['OT'] = df['OT'].astype(str)
            df.loc[df['OT'].str.contains('OT', na=False), 'OT'] = 1
            df['OT'] = pd.to_numeric(df['OT'], errors='coerce').fillna(0).astype(int)

    if 'Opp' in df.columns:
        df = df[df['Opp'] != 'Opp']
        df = df[df['Opp'].notna()]

    return df

