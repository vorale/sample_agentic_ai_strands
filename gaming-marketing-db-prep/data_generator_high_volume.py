#!/usr/bin/env python3
"""
High-volume data generator for gaming marketing database
Generates 50k+ rows across all tables for realistic testing
"""

import mysql.connector
import random
import datetime
import uuid
import json
from faker import Faker
import os
from dotenv import load_dotenv
import time

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

device_types = ["Mobile", "Tablet", "Desktop"]
os_versions = ["iOS 16", "iOS 17", "Android 12", "Android 13", "Android 14"]
countries = ["US", "UK", "CA", "AU", "DE", "FR", "JP", "KR", "BR", "IN"]
acquisition_sources = ["Facebook", "Google", "AppLovin", "Unity", "TikTok", "Snapchat", "Twitter"]

event_types = [
    "level_start", "level_complete", "level_fail", "purchase", "ad_view", 
    "tutorial_start", "tutorial_complete", "achievement_unlock", "social_share",
    "settings_change", "app_crash", "session_timeout"
]

game_names = [
    "Dragon Quest Mobile", "Puzzle Kingdom", "Racing Thunder", "Battle Arena",
    "Farm Paradise", "City Builder Pro", "Space Adventure", "Card Master",
    "Cooking Fever", "Match Three Saga"
]

platform_names = [
    "Facebook Ads", "Google Ads", "AppLovin", "Unity Ads", "TikTok Ads",
    "Snapchat Ads", "Twitter Ads", "Apple Search Ads"
]

def generate_base_data(cursor):
    """Generate base reference data (games, platforms)"""
    print("Generating base reference data...")
    
    # Generate games
    games = []
    for i, game_name in enumerate(game_names, 1):
        games.append((i, game_name, fake.company(), fake.date_between(start_date='-2y', end_date='today')))
    
    cursor.executemany("""
        INSERT IGNORE INTO games (game_id, game_name, developer, release_date) 
        VALUES (%s, %s, %s, %s)
    """, games)
    
    # Generate ad platforms
    platforms = []
    for i, platform_name in enumerate(platform_names, 1):
        platforms.append((i, platform_name))
    
    cursor.executemany("""
        INSERT IGNORE INTO ad_platforms (platform_id, platform_name) 
        VALUES (%s, %s)
    """, platforms)
    
    print(f"Generated {len(games)} games and {len(platforms)} platforms")

def generate_campaigns(cursor, num_campaigns=500):
    """Generate campaigns"""
    print(f"Generating {num_campaigns} campaigns...")
    
    campaigns = []
    for i in range(num_campaigns):
        game_id = random.randint(1, len(game_names))
        platform_id = random.randint(1, len(platform_names))
        start_date = fake.date_between(start_date='-1y', end_date='today')
        end_date = fake.date_between(start_date=start_date, end_date='+30d')
        
        campaigns.append((
            f"Campaign_{game_names[game_id-1]}_{platform_names[platform_id-1]}_{i}",
            game_id,
            platform_id,
            start_date,
            end_date,
            round(random.uniform(1000, 50000), 2),
            random.choice(campaign_status),
            random.choice(campaign_objectives)
        ))
    
    cursor.executemany("""
        INSERT INTO campaigns 
        (campaign_name, game_id, platform_id, start_date, end_date, budget, status, objective) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, campaigns)
    
    print(f"Inserted {len(campaigns)} campaigns")

def generate_ad_creatives(cursor, num_creatives=2000):
    """Generate ad creatives"""
    print(f"Generating {num_creatives} ad creatives...")
    
    # Get campaign IDs
    cursor.execute("SELECT campaign_id FROM campaigns")
    campaign_ids = [row[0] for row in cursor.fetchall()]
    
    creatives = []
    for i in range(num_creatives):
        campaign_id = random.choice(campaign_ids)
        creative_type = random.choice(creative_types)
        
        creatives.append((
            campaign_id,
            f"Creative_{creative_type}_{i}",
            creative_type,
            f"https://cdn.example.com/creatives/{creative_type.lower()}_{i}.jpg",
            f"{random.choice([320, 480, 720, 1080])}x{random.choice([480, 720, 1080, 1920])}",
            random.randint(15, 60) if creative_type == "Video" else None
        ))
    
    cursor.executemany("""
        INSERT INTO ad_creatives 
        (campaign_id, creative_name, creative_type, creative_url, dimensions, duration) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, creatives)
    
    print(f"Inserted {len(creatives)} ad creatives")

def generate_user_sessions(cursor, num_sessions=10000):
    """Generate user sessions"""
    print(f"Generating {num_sessions} user sessions...")
    
    sessions = []
    user_ids = []
    
    for i in range(num_sessions):
        user_id = f"user_{random.randint(1, num_sessions//5)}"  # Create some repeat users
        user_ids.append(user_id)
        
        session_start = fake.date_time_between(start_date='-90d', end_date='now')
        session_duration = random.randint(30, 3600)  # 30 seconds to 1 hour
        session_end = session_start + datetime.timedelta(seconds=session_duration)
        
        sessions.append((
            str(uuid.uuid4()),
            user_id,
            random.randint(1, len(game_names)),
            session_start,
            session_end,
            session_duration,
            random.choice(device_types),
            random.choice(os_versions),
            random.choice(countries),
            random.choice(acquisition_sources)
        ))
    
    # Insert in batches
    batch_size = 1000
    for i in range(0, len(sessions), batch_size):
        batch = sessions[i:i+batch_size]
        cursor.executemany("""
            INSERT INTO user_sessions 
            (session_id, user_id, game_id, session_start, session_end, session_duration, 
             device_type, os_version, country, acquisition_source) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, batch)
        print(f"Inserted batch {i//batch_size + 1} of user sessions")
    
    print(f"Inserted {len(sessions)} user sessions")
    
    # Return session data for event generation
    cursor.execute("SELECT session_id, user_id, game_id FROM user_sessions")
    return cursor.fetchall()

def generate_in_game_events(cursor, session_data, events_per_session=5):
    """Generate in-game events"""
    total_events = len(session_data) * events_per_session
    print(f"Generating approximately {total_events} in-game events...")
    
    all_events = []
    
    for session_id, user_id, game_id in session_data:
        num_events = random.randint(1, events_per_session * 2)  # Vary events per session
        
        for _ in range(num_events):
            event_type = random.choice(event_types)
            
            all_events.append((
                str(uuid.uuid4()),
                session_id,
                user_id,
                game_id,
                event_type,
                fake.date_time_between(start_date='-90d', end_date='now'),
                random.randint(1, 100) if 'level' in event_type else None,
                round(random.uniform(0, 1000), 2) if event_type == 'purchase' else random.randint(1, 100),
                json.dumps({
                    "source": random.choice(["organic", "paid"]),
                    "difficulty": random.choice(["easy", "medium", "hard"]),
                    "success": random.choice([True, False])
                })
            ))
    
    # Insert in batches
    batch_size = 1000
    for i in range(0, len(all_events), batch_size):
        batch = all_events[i:i+batch_size]
        cursor.executemany("""
            INSERT INTO in_game_events 
            (event_id, session_id, user_id, game_id, event_type, event_timestamp, 
             level_id, event_value, event_details) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, batch)
        print(f"Inserted batch {i//batch_size + 1} of in-game events")
    
    print(f"Inserted {len(all_events)} in-game events")

def generate_ad_performance(cursor, num_records=5000):
    """Generate ad performance data"""
    print(f"Generating {num_records} ad performance records...")
    
    # Get campaign IDs, creative IDs, and platform IDs
    cursor.execute("SELECT campaign_id FROM campaigns")
    campaign_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT creative_id, campaign_id FROM ad_creatives")
    creative_data = cursor.fetchall()
    
    cursor.execute("SELECT platform_id FROM ad_platforms")
    platform_ids = [row[0] for row in cursor.fetchall()]
    
    performance_data = []
    for i in range(num_records):
        # Pick a creative and its associated campaign
        creative_id, campaign_id = random.choice(creative_data)
        platform_id = random.choice(platform_ids)
        
        impressions = random.randint(1000, 100000)
        clicks = random.randint(10, impressions // 10)
        installs = random.randint(1, clicks // 5)
        spend = round(random.uniform(100, 5000), 2)
        
        performance_data.append((
            campaign_id,
            creative_id,
            platform_id,
            fake.date_between(start_date='-90d', end_date='today'),
            impressions,
            clicks,
            installs,
            spend,
            round((clicks / impressions) * 100, 2),  # CTR
            round(spend / installs if installs > 0 else 0, 2),  # CPI
            round(random.uniform(0.5, 5.0), 2)  # ROAS
        ))
    
    # Insert in batches
    batch_size = 1000
    for i in range(0, len(performance_data), batch_size):
        batch = performance_data[i:i+batch_size]
        cursor.executemany("""
            INSERT INTO ad_performance 
            (campaign_id, creative_id, platform_id, date, impressions, clicks, installs, spend, ctr, cpi, roas) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, batch)
        print(f"Inserted batch {i//batch_size + 1} of ad performance records")
    
    print(f"Inserted {len(performance_data)} ad performance records")

def generate_purchase_events(cursor, num_purchases=3000):
    """Generate purchase events"""
    print(f"Generating {num_purchases} purchase events...")
    
    # Get session data for purchases
    cursor.execute("SELECT session_id, user_id, game_id FROM user_sessions LIMIT 1000")
    session_data = cursor.fetchall()
    
    product_types = ["coins", "gems", "power_ups", "characters", "levels", "remove_ads", "premium_pass"]
    payment_providers = ["Apple", "Google", "PayPal", "Stripe", "Amazon"]
    
    purchases = []
    for i in range(num_purchases):
        session_id, user_id, game_id = random.choice(session_data)
        product_type = random.choice(product_types)
        
        # Price varies by product type
        price_ranges = {
            "coins": (0.99, 9.99),
            "gems": (1.99, 19.99),
            "power_ups": (0.99, 4.99),
            "characters": (2.99, 14.99),
            "levels": (1.99, 9.99),
            "remove_ads": (2.99, 4.99),
            "premium_pass": (9.99, 29.99)
        }
        
        price = round(random.uniform(*price_ranges[product_type]), 2)
        
        purchases.append((
            str(uuid.uuid4()),  # purchase_id
            session_id,         # session_id
            user_id,           # user_id
            game_id,           # game_id
            f"{product_type}_{random.randint(1, 100)}",  # product_id
            product_type,      # product_type
            fake.date_time_between(start_date='-90d', end_date='now'),  # purchase_timestamp
            random.choice(["USD", "EUR", "GBP", "JPY"]),  # currency
            price,             # price
            random.choice(payment_providers),  # payment_provider
            f"txn_{uuid.uuid4().hex[:12]}",   # transaction_id
            random.choice([0, 1])  # is_first_purchase
        ))
    
    # Insert in batches
    batch_size = 1000
    for i in range(0, len(purchases), batch_size):
        batch = purchases[i:i+batch_size]
        cursor.executemany("""
            INSERT INTO purchase_events 
            (purchase_id, session_id, user_id, game_id, product_id, product_type, 
             purchase_timestamp, currency, price, payment_provider, transaction_id, is_first_purchase) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, batch)
        print(f"Inserted batch {i//batch_size + 1} of purchase events")
    
    print(f"Inserted {len(purchases)} purchase events")

def main():
    """Main execution with high volume data generation"""
    start_time = time.time()
    conn, cursor = connect_to_db()
    
    try:
        print("=== HIGH VOLUME DATA GENERATION ===")
        print("Target: 50,000+ total rows")
        print()
        
        # Generate base data
        generate_base_data(cursor)
        conn.commit()
        
        # Generate campaigns (500 campaigns)
        generate_campaigns(cursor, num_campaigns=500)
        conn.commit()
        
        # Generate ad creatives (2000 creatives)
        generate_ad_creatives(cursor, num_creatives=2000)
        conn.commit()
        
        # Generate user sessions (10000 sessions)
        session_data = generate_user_sessions(cursor, num_sessions=10000)
        conn.commit()
        
        # Generate in-game events (~50000 events, 5 per session average)
        generate_in_game_events(cursor, session_data, events_per_session=5)
        conn.commit()
        
        # Generate ad performance data (5000 records)
        generate_ad_performance(cursor, num_records=5000)
        conn.commit()
        
        # Generate purchase events (3000 purchases)
        generate_purchase_events(cursor, num_purchases=3000)
        conn.commit()
        
        print("\n=== DATA GENERATION COMPLETE ===")
        
        # Verify data
        print("\nFinal row counts:")
        tables = [
            "games", "ad_platforms", "campaigns", "ad_creatives", 
            "user_sessions", "in_game_events", "ad_performance", "purchase_events"
        ]
        
        total_rows = 0
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            total_rows += count
            print(f"{table}: {count:,}")
        
        print(f"\nTOTAL ROWS: {total_rows:,}")
        
        elapsed_time = time.time() - start_time
        print(f"Generation time: {elapsed_time:.2f} seconds")
        
        if total_rows >= 50000:
            print("✅ SUCCESS: Generated 50k+ rows!")
        else:
            print(f"⚠️  Generated {total_rows:,} rows (target was 50k+)")
        
    except Exception as e:
        print(f"Error during data generation: {e}")
        conn.rollback()
        raise
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    main()
