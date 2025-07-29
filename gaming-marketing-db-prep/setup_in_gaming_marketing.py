#!/usr/bin/env python3
"""
Script to create gaming marketing tables in the existing gaming_marketing database
"""

import mysql.connector
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MySQL connection parameters for gaming_marketing
config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'mcpuser'),
    'password': os.getenv('MYSQL_PASSWORD', 'mcppassword'),
    'database': 'gaming_marketing'
}

def read_sql_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        # Remove CREATE DATABASE and USE statements
        lines = content.split('\n')
        filtered_lines = []
        skip_next = False
        for line in lines:
            if "CREATE DATABASE" in line or "USE " in line:
                skip_next = True
                continue
            if skip_next and ";" in line:
                skip_next = False
                continue
            # Skip SHOW TABLES statement at the end
            if "SHOW TABLES" in line:
                continue
            filtered_lines.append(line)
        return '\n'.join(filtered_lines)

try:
    # Connect to MySQL
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print(f"Connected to MySQL database: {config['database']}")
    
    # Read SQL file but skip CREATE DATABASE and USE statements
    sql_path = os.path.join(os.path.dirname(__file__), 'gaming_marketing_schema.sql')
    sql_content = read_sql_file(sql_path)
    
    # Split SQL statements
    statements = sql_content.split(';')
    
    # Execute each statement
    for statement in statements:
        statement = statement.strip()
        if statement:
            try:
                cursor.execute(statement)
                print(f"Executed: {statement[:50]}...")
            except mysql.connector.Error as err:
                print(f"Error executing: {statement[:50]}...")
                print(f"Error: {err}")
    
    conn.commit()
    print("Tables created successfully in gaming_marketing database")
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
    sys.exit(1)
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection closed")
