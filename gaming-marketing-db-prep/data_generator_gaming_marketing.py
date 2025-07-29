#!/usr/bin/env python3
"""
Data generator for gaming marketing database tables in gaming-market
"""

import mysql.connector
import random
import datetime
import uuid
import json
from faker import Faker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MySQL connection parameters
config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'mcpuser'),
    'password': os.getenv('MYSQL_PASSWORD', 'mcppassword'),
    'database': 'gaming_marketing'
}

# Initialize Faker
fake = Faker()

# Connect to MySQL
def connect_to_db():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        print("Connected to MySQL database")
        return conn, cursor
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        exit(1)

# Sample data
campaign_objectives = [
    "Acquisition", "Retention", "Monetization", "Brand awareness", 
    "App installs", "Engagement", "Re-engagement"
]

campaign_status = ["Active", "Paused", "Completed"]

creative_types = [
    "Video", "Image", "Playable", "Carousel", "Story", 
    "Banner", "Interstitial", "Native"
]

countries = [
    "US", "GB", "CA", "AU", "DE", "FR", "JP", "KR", 
    "BR", "MX", "IN", "RU", "IT", "ES", "CN"
]

device_types = [
    "iPhone", "iPad", "Android Phone", "Android Tablet", 
    "Samsung Galaxy", "Google Pixel", "Huawei", "Xiaomi"
]

os_versions = [
    "iOS 14", "iOS 15", "iOS 16", "Android 10", "Android 11", 
    "Android 12", "Android 13"
]

ad_formats = [
    "Interstitial", "Rewarded", "Banner", "Native", 
    "Playable", "Video"
]

event_types = [
    "level_start", "level_complete", "level_fail", "item_purchase", 
    "tutorial_start", "tutorial_complete", "achievement_unlocked", 
    "daily_reward_claimed", "character_upgrade", "store_opened",
    "ad_offered", "ad_started", "ad_completed", "ad_skipped",
    "login", "logout", "friend_invite", "friend_accept"
]

# Generate campaigns
def generate_campaigns(cursor, num_campaigns=20):
    print(f"Generating {num_campaigns} campaigns...")
    
    # Get game IDs
    cursor.execute("SELECT game_id FROM games")
    game_ids = [row[0] for row in cursor.fetchall()]
    
    # Get platform IDs
    cursor.execute("SELECT platform_id FROM ad_platforms")
    platform_ids = [row[0] for row in cursor.fetchall()]
    
    campaigns = []
    
    for i in range(num_campaigns):
        game_id = random.choice(game_ids)
        platform_id = random.choice(platform_ids)
        
        # Generate campaign name
        campaign_name = f"Campaign {i+1} - {fake.word().capitalize()} {random.choice(['Boost', 'Growth', 'Promo', 'Launch'])}"
        
        # Generate dates
        start_date = fake.date_between(start_date='-1y', end_date='today')
        
        # Some campaigns are ongoing, some have end dates
        if random.random() < 0.7:
            end_date = fake.date_between(start_date=start_date, end_date='+6m')
            end_date_str = end_date.strftime('%Y-%m-%d')
        else:
            end_date_str = None
        
        # Generate budget
        budget = round(random.uniform(1000, 100000), 2)
        
        # Generate status and objective
        status = random.choice(campaign_status)
        objective = random.choice(campaign_objectives)
        
        campaigns.append((
            campaign_name, 
            game_id, 
            platform_id, 
            start_date.strftime('%Y-%m-%d'), 
            end_date_str, 
            budget, 
            status, 
            objective
        ))
    
    # Insert campaigns into database
    insert_query = """
    INSERT INTO campaigns 
    (campaign_name, game_id, platform_id, start_date, end_date, budget, status, objective) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_query, campaigns)
    
    print(f"Inserted {len(campaigns)} campaigns")

# Generate ad creatives
def generate_ad_creatives(cursor, num_creatives=50):
    print(f"Generating {num_creatives} ad creatives...")
    
    # Get campaign IDs
    cursor.execute("SELECT campaign_id FROM campaigns")
    campaign_ids = [row[0] for row in cursor.fetchall()]
    
    creatives = []
    
    for i in range(num_creatives):
        campaign_id = random.choice(campaign_ids)
        
        # Generate creative name
        creative_name = f"Creative {i+1} - {fake.word().capitalize()} {random.choice(['Ad', 'Promo', 'Visual'])}"
        
        # Generate creative type and related attributes
        creative_type = random.choice(creative_types)
        
        # Generate URL
        creative_url = f"https://assets.example.com/creatives/{fake.uuid4()}.{random.choice(['mp4', 'jpg', 'png', 'html'])}"
        
        # Generate dimensions based on type
        if creative_type in ["Image", "Banner"]:
            dimensions = random.choice(["1200x628", "1080x1080", "320x50", "300x250"])
        elif creative_type == "Video":
            dimensions = random.choice(["1920x1080", "1280x720", "640x480"])
        else:
            dimensions = None
        
        # Generate duration for video
        duration = random.randint(15, 60) if creative_type == "Video" else None
        
        creatives.append((
            campaign_id,
            creative_name,
            creative_type,
            creative_url,
            dimensions,
            duration
        ))
    
    # Insert creatives into database
    insert_query = """
    INSERT INTO ad_creatives 
    (campaign_id, creative_name, creative_type, creative_url, dimensions, duration) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_query, creatives)
    
    print(f"Inserted {len(creatives)} ad creatives")

# Generate user sessions
def generate_user_sessions(cursor, num_sessions=100):
    print(f"Generating {num_sessions} user sessions...")
    
    # Get game IDs
    cursor.execute("SELECT game_id FROM games")
    game_ids = [row[0] for row in cursor.fetchall()]
    
    sessions = []
    
    for i in range(num_sessions):
        # Generate UUIDs
        session_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())
        
        # Select game
        game_id = random.choice(game_ids)
        
        # Generate timestamps
        session_start = fake.date_time_between(start_date='-30d', end_date='now')
        
        # 90% of sessions have ended, 10% are ongoing
        if random.random() < 0.9:
            session_duration = random.randint(30, 3600)  # 30 seconds to 1 hour
            session_end = session_start + datetime.timedelta(seconds=session_duration)
        else:
            session_duration = None
            session_end = None
        
        # Generate device info
        device_type = random.choice(device_types)
        os_version = random.choice(os_versions)
        country = random.choice(countries)
        
        # Generate acquisition source
        acquisition_source = random.choice(['Facebook', 'Google', 'AppLovin', 'Organic', 'Apple Search Ads'])
        
        sessions.append((
            session_id,
            user_id,
            game_id,
            session_start,
            session_end,
            session_duration,
            device_type,
            os_version,
            country,
            acquisition_source
        ))
    
    # Insert sessions into database
    insert_query = """
    INSERT INTO user_sessions 
    (session_id, user_id, game_id, session_start, session_end, session_duration, 
     device_type, os_version, country, acquisition_source) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_query, sessions)
    
    print(f"Inserted {len(sessions)} user sessions")
    
    # Return session IDs and user IDs for other event generation
    return [(s[0], s[1], s[2]) for s in sessions]  # session_id, user_id, game_id

# Generate in-game events
def generate_in_game_events(cursor, session_data, events_per_session=5):
    print(f"Generating in-game events for {len(session_data)} sessions...")
    
    all_events = []
    
    for session_id, user_id, game_id in session_data:
        # Get session start time
        cursor.execute("SELECT session_start FROM user_sessions WHERE session_id = %s", (session_id,))
        session_start = cursor.fetchone()[0]
        
        # Generate random number of events for this session
        num_events = random.randint(1, events_per_session)
        
        for _ in range(num_events):
            # Generate event ID
            event_id = str(uuid.uuid4())
            
            # Generate event type
            event_type = random.choice(event_types)
            
            # Generate timestamp within session
            minutes_offset = random.randint(0, 30)
            event_timestamp = session_start + datetime.timedelta(minutes=minutes_offset)
            
            # Generate level ID if applicable
            level_id = f"level_{random.randint(1, 100)}" if "level" in event_type else None
            
            # Generate event value if applicable
            event_value = round(random.uniform(1, 1000), 2) if random.random() < 0.5 else None
            
            # Generate event details as JSON
            details = {
                "location": f"screen_{random.randint(1, 10)}",
                "duration": random.randint(1, 60),
                "result": random.choice(["success", "failure", "incomplete"])
            }
            
            if "purchase" in event_type:
                details["item_id"] = f"item_{random.randint(1, 100)}"
                details["currency"] = random.choice(["USD", "EUR", "GBP", "JPY"])
                details["amount"] = round(random.uniform(0.99, 99.99), 2)
            
            event_details = json.dumps(details)
            
            all_events.append((
                event_id,
                session_id,
                user_id,
                game_id,
                event_type,
                event_timestamp,
                level_id,
                event_value,
                event_details
            ))
    
    # Insert in batches to avoid memory issues
    batch_size = 100
    for i in range(0, len(all_events), batch_size):
        batch = all_events[i:i+batch_size]
        
        insert_query = """
        INSERT INTO in_game_events 
        (event_id, session_id, user_id, game_id, event_type, event_timestamp, 
         level_id, event_value, event_details) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, batch)
        print(f"Inserted batch of {len(batch)} in-game events")
    
    print(f"Inserted a total of {len(all_events)} in-game events")

# Main execution
def main():
    conn, cursor = connect_to_db()
    
    try:
        # Generate campaigns
        generate_campaigns(cursor, num_campaigns=10)
        conn.commit()
        
        # Generate ad creatives
        generate_ad_creatives(cursor, num_creatives=20)
        conn.commit()
        
        # Generate user sessions
        session_data = generate_user_sessions(cursor, num_sessions=50)
        conn.commit()
        
        # Generate in-game events
        generate_in_game_events(cursor, session_data, events_per_session=3)
        conn.commit()
        
        print("Data generation complete!")
        
        # Verify data
        print("\nVerifying data:")
        cursor.execute("SELECT COUNT(*) FROM campaigns")
        print(f"Campaigns: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM ad_creatives")
        print(f"Ad Creatives: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM user_sessions")
        print(f"User Sessions: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM in_game_events")
        print(f"In-game Events: {cursor.fetchone()[0]}")
        
    except Exception as e:
        print(f"Error during data generation: {e}")
        conn.rollback()
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    main()
