# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 15:47:30 2025

@author: Logmo
"""

#%% import libraries
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
#%% Import csv files




# #%% Get all csv gamelogs and combine them into dataframe
# load_dotenv("C:/Users/Logmo/cbb-money/.env")
# engine = create_engine(f'mysql+mysqlconnector://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}')

# query = "SELECT * FROM season_stats;"
# df_season_stats = pd.read_sql(query,engine)

# print(df_season_stats.head())



