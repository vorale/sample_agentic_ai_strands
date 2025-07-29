#!/usr/bin/env python3
"""
Script to verify data in the gaming marketing database
"""

import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MySQL connection parameters
config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'mcpuser'),
    'password': os.getenv('MYSQL_PASSWORD', 'mcppassword'),
    'database': 'mcpdb'
}

# Connect to MySQL
conn = mysql.connector.connect(**config)
cursor = conn.cursor(dictionary=True)
print(f"Connected to MySQL database: {config['database']}")

# Check games table
cursor.execute("SELECT * FROM games LIMIT 5")
games = cursor.fetchall()
print("\nSample games data:")
for game in games:
    print(game)

# Check campaigns table
cursor.execute("SELECT * FROM campaigns LIMIT 5")
campaigns = cursor.fetchall()
print("\nSample campaigns data:")
for campaign in campaigns:
    print(campaign)

# Check ad creatives table
cursor.execute("SELECT * FROM ad_creatives LIMIT 5")
creatives = cursor.fetchall()
print("\nSample ad creatives data:")
for creative in creatives:
    print(creative)

# Check user sessions table
cursor.execute("SELECT * FROM user_sessions LIMIT 5")
sessions = cursor.fetchall()
print("\nSample user sessions data:")
for session in sessions:
    print(session)

# Check in-game events table
cursor.execute("SELECT * FROM in_game_events LIMIT 5")
events = cursor.fetchall()
print("\nSample in-game events data:")
for event in events:
    print(event)

# Count records in each table
tables = [
    'games', 'ad_platforms', 'campaigns', 'ad_creatives', 
    'user_sessions', 'in_game_events'
]

print("\nRecord counts:")
for table in tables:
    cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
    count = cursor.fetchone()['count']
    print(f"{table}: {count} records")

# Close connection
cursor.close()
conn.close()
print("\nMySQL connection closed")
