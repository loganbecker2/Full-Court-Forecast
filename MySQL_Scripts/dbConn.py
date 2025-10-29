# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 12:48:51 2025

@author: Logmo
"""

#%% connect to mysql db
import MySQLdb
import os
from dotenv import load_dotenv


# Load .env file
load_dotenv()

# Connect to the MySQL database
conn = MySQLdb.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Create a cursor
cursor = conn.cursor()

# Test a simple query
cursor.execute("SELECT DATABASE()")
current_db = cursor.fetchone()
print("Connected to database:", current_db)

# Clean up
cursor.close()
conn.close()

# %%
