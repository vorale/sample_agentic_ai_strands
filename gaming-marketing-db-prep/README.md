# Gaming Marketing Database

This folder contains scripts to set up a MySQL database for gaming marketing analytics. The database is designed to store and analyze marketing data from various ad platforms (Facebook, Google, AppLovin, etc.) for mobile games.

## Database Structure

The database includes tables for:

1. **Aggregated Marketing Data**:
   - Campaigns
   - Ad Creatives
   - Ad Performance
   - User Acquisition
   - User Retention
   - Monetization
   - Ad Network Revenue
   - Cohort Analysis

2. **Granular Event Telemetry**:
   - User Sessions
   - In-Game Events
   - Ad Engagement Events
   - Purchase Events
   - Progression Events
   - Social Events
   - Attribution Events
   - Feature Usage Events
   - Error Events
   - User Segments

## Complete Setup Guide

### Prerequisites

- Docker Desktop installed and running
- Python 3.7+ with pip
- Git (for cloning the repository)

### Step 1: Docker MySQL Container Setup

#### Option A: Using Docker Compose (Recommended)

1. **Start the MySQL container**:
```bash
docker-compose up -d
```

This will:
- Create a MySQL 8.0 container named `gaming-marketing-mysql`
- Set up the database with proper credentials
- Create the `gaming_marketing` database
- Configure the `mcpuser` with appropriate permissions

#### Option B: Manual Docker Setup

1. **Create and run MySQL container**:
```bash
docker run -d \
  --name gaming-marketing-mysql \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -e MYSQL_DATABASE=gaming_marketing \
  -e MYSQL_USER=mcpuser \
  -e MYSQL_PASSWORD=mcppassword \
  -p 3306:3306 \
  mysql:8.0
```

2. **Verify container is running**:
```bash
docker ps | grep mysql
```

### Step 2: Environment Configuration

1. **Set environment variables**:
```bash
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=mcpuser
export MYSQL_PASSWORD=mcppassword
export MYSQL_DATABASE=gaming_marketing
```

Or use the Docker environment file:
```bash
source .env.docker
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

### Step 3: Database Schema Creation

1. **Create all database tables**:
```bash
MYSQL_HOST=localhost MYSQL_USER=mcpuser MYSQL_PASSWORD=mcppassword MYSQL_DATABASE=gaming_marketing python setup_in_gaming_marketing.py
```

This will create all tables including:
- Reference tables (games, ad_platforms)
- Campaign and creative tables
- User behavior tables (sessions, events)
- Performance and analytics tables

### Step 4: Data Generation

#### Option A: High-Volume Data (80k+ rows) - Recommended

Generate realistic volume data for testing and analysis:

```bash
MYSQL_HOST=localhost MYSQL_USER=mcpuser MYSQL_PASSWORD=mcppassword MYSQL_DATABASE=gaming_marketing python data_generator_high_volume.py
```

This generates:
- **500 campaigns** across multiple ad platforms
- **2,000 ad creatives** with various formats
- **10,000 user sessions** with realistic patterns
- **54,000+ in-game events** tracking user behavior
- **10,000 ad performance records** with metrics
- **3,000 purchase events** for monetization analysis

**Total: ~80,000 rows**

#### Option B: Small Sample Data

For quick testing with minimal data:

```bash
MYSQL_HOST=localhost MYSQL_USER=mcpuser MYSQL_PASSWORD=mcppassword MYSQL_DATABASE=gaming_marketing python data_generator_gaming_marketing.py
```

This generates ~230 rows for basic testing.

### Step 5: Data Verification

1. **Verify data was created successfully**:
```bash
MYSQL_HOST=localhost MYSQL_USER=mcpuser MYSQL_PASSWORD=mcppassword MYSQL_DATABASE=gaming_marketing python verify_data.py
```

2. **Check row counts directly**:
```bash
docker exec gaming-marketing-mysql mysql -u mcpuser -p'mcppassword' gaming_marketing -e "
SELECT 
  'campaigns' as table_name, COUNT(*) as row_count FROM campaigns
UNION ALL SELECT 'ad_creatives', COUNT(*) FROM ad_creatives
UNION ALL SELECT 'user_sessions', COUNT(*) FROM user_sessions
UNION ALL SELECT 'in_game_events', COUNT(*) FROM in_game_events
UNION ALL SELECT 'ad_performance', COUNT(*) FROM ad_performance
UNION ALL SELECT 'purchase_events', COUNT(*) FROM purchase_events;
"
```

### Step 6: Database Access

#### Connect via MySQL Client
```bash
docker exec -it gaming-marketing-mysql mysql -u mcpuser -p'mcppassword' gaming_marketing
```

#### Connect from External Tools
- **Host**: localhost
- **Port**: 3306
- **Database**: gaming_marketing
- **Username**: mcpuser
- **Password**: mcppassword

## Detailed Step-by-Step Setup

### Complete Setup from Scratch

Follow these detailed steps to set up the gaming marketing database from a fresh system:

#### 1. Initial Setup and Prerequisites

1. **Ensure Docker is installed and running**:
```bash
# Check if Docker is running
docker --version
docker ps
```

2. **Clone or download this repository**:
```bash
# If using git
git clone <repository-url>
cd gaming-marketing-db-prep

# Or download and extract the files to this directory
```

3. **Install Python dependencies**:
```bash
pip install -r requirements-data-gen.txt
```

#### 2. Docker Container Creation

**Option A: Using Docker Compose (Recommended)**

1. **Review the docker-compose.yml configuration**:
```bash
cat docker-compose.yml
```

2. **Start the MySQL container**:
```bash
docker-compose up -d
```

3. **Verify container is running**:
```bash
docker-compose ps
```

**Option B: Manual Docker Container Creation**

1. **Create MySQL container manually**:
```bash
docker run -d \
  --name gaming-marketing-mysql \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -e MYSQL_DATABASE=gaming_marketing \
  -e MYSQL_USER=mcpuser \
  -e MYSQL_PASSWORD=mcppassword \
  -p 3306:3306 \
  mysql:8.0
```

2. **Wait for MySQL to initialize** (about 30-60 seconds):
```bash
# Check container logs to see when it's ready
docker logs gaming-marketing-mysql

# Look for: "MySQL init process done. Ready for start up."
```

3. **Verify container is running**:
```bash
docker ps | grep mysql
```

#### 3. Database User and Permissions Verification

1. **Test root connection**:
```bash
docker exec gaming-marketing-mysql mysql -u root -p'123456' -e "SHOW DATABASES;"
```

2. **Verify mcpuser exists and has permissions**:
```bash
docker exec gaming-marketing-mysql mysql -u root -p'123456' -e "SHOW GRANTS FOR 'mcpuser'@'%';"
```

3. **Test mcpuser connection**:
```bash
docker exec gaming-marketing-mysql mysql -u mcpuser -p'mcppassword' gaming_marketing -e "SHOW TABLES;"
```

#### 4. Environment Configuration

1. **Set environment variables for the session**:
```bash
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=mcpuser
export MYSQL_PASSWORD=mcppassword
export MYSQL_DATABASE=gaming_marketing
```

2. **Or use the provided environment file**:
```bash
# Load Docker environment variables
source .env.docker

# Verify variables are set
echo "Host: $MYSQL_HOST, User: $MYSQL_USER, Database: $MYSQL_DATABASE"
```

#### 5. Database Schema Creation

1. **Create all database tables**:
```bash
MYSQL_HOST=localhost MYSQL_USER=mcpuser MYSQL_PASSWORD=mcppassword MYSQL_DATABASE=gaming_marketing python setup_in_gaming_marketing.py
```

2. **Verify tables were created**:
```bash
docker exec gaming-marketing-mysql mysql -u mcpuser -p'mcppassword' gaming_marketing -e "SHOW TABLES;"
```

3. **Check table structure (optional)**:
```bash
docker exec gaming-marketing-mysql mysql -u mcpuser -p'mcppassword' gaming_marketing -e "DESCRIBE campaigns;"
```

#### 6. Data Generation

**For High-Volume Data (80k+ rows) - Recommended:**

1. **Generate comprehensive dataset**:
```bash
MYSQL_HOST=localhost MYSQL_USER=mcpuser MYSQL_PASSWORD=mcppassword MYSQL_DATABASE=gaming_marketing python data_generator_high_volume.py
```

2. **Expected output**:
```
=== HIGH VOLUME DATA GENERATION ===
Target: 50,000+ total rows

Generating base reference data...
Generated 10 games and 8 platforms
Generating 500 campaigns...
Inserted 500 campaigns
Generating 2000 ad creatives...
Inserted 2000 ad creatives
Generating 10000 user sessions...
[... batch processing ...]
Inserted 10000 user sessions
Generating approximately 50000 in-game events...
[... batch processing ...]
Inserted 54732 in-game events
Generating 5000 ad performance records...
[... batch processing ...]
Inserted 5000 ad performance records
Generating 3000 purchase events...
[... batch processing ...]
Inserted 3000 purchase events

=== FINAL DATA COUNTS ===
games: 10
ad_platforms: 8
campaigns: 500
ad_creatives: 2,000
user_sessions: 10,000
in_game_events: 54,732
ad_performance: 5,000
purchase_events: 3,000

TOTAL ROWS: 80,250
✅ SUCCESS: Generated 50k+ rows!
```

**For Small Sample Data (230 rows):**

1. **Generate minimal dataset for testing**:
```bash
MYSQL_HOST=localhost MYSQL_USER=mcpuser MYSQL_PASSWORD=mcppassword MYSQL_DATABASE=gaming_marketing python data_generator_gaming_marketing.py
```

#### 7. Data Verification and Testing

1. **Run verification script**:
```bash
MYSQL_HOST=localhost MYSQL_USER=mcpuser MYSQL_PASSWORD=mcppassword MYSQL_DATABASE=gaming_marketing python verify_data.py
```

2. **Manual data verification**:
```bash
docker exec gaming-marketing-mysql mysql -u mcpuser -p'mcppassword' gaming_marketing -e "
SELECT 
  'games' as table_name, COUNT(*) as row_count FROM games
UNION ALL SELECT 'ad_platforms', COUNT(*) FROM ad_platforms
UNION ALL SELECT 'campaigns', COUNT(*) FROM campaigns
UNION ALL SELECT 'ad_creatives', COUNT(*) FROM ad_creatives
UNION ALL SELECT 'user_sessions', COUNT(*) FROM user_sessions
UNION ALL SELECT 'in_game_events', COUNT(*) FROM in_game_events
UNION ALL SELECT 'ad_performance', COUNT(*) FROM ad_performance
UNION ALL SELECT 'purchase_events', COUNT(*) FROM purchase_events
ORDER BY row_count DESC;
"
```

3. **Test sample queries**:
```bash
docker exec gaming-marketing-mysql mysql -u mcpuser -p'mcppassword' gaming_marketing -e "
SELECT 
    c.campaign_name,
    g.game_name,
    COUNT(ap.performance_id) as performance_records,
    SUM(ap.impressions) as total_impressions,
    SUM(ap.clicks) as total_clicks,
    SUM(ap.installs) as total_installs
FROM campaigns c
JOIN games g ON c.game_id = g.game_id
LEFT JOIN ad_performance ap ON c.campaign_id = ap.campaign_id
GROUP BY c.campaign_id
LIMIT 10;
"
```

#### 8. Database Access and Connection

1. **Connect via MySQL client in container**:
```bash
docker exec -it gaming-marketing-mysql mysql -u mcpuser -p'mcppassword' gaming_marketing
```

2. **Connect from external MySQL client**:
   - **Host**: localhost
   - **Port**: 3306
   - **Database**: gaming_marketing
   - **Username**: mcpuser
   - **Password**: mcppassword

3. **Test external connection**:
```bash
# If you have mysql client installed locally
mysql -h localhost -P 3306 -u mcpuser -p'mcppassword' gaming_marketing
```

#### 9. Common Issues and Solutions

**Issue: Container won't start**
```bash
# Check if port 3306 is already in use
lsof -i :3306

# Stop any existing MySQL services
sudo service mysql stop  # Linux
brew services stop mysql  # macOS

# Remove existing container and recreate
docker stop gaming-marketing-mysql
docker rm gaming-marketing-mysql
# Then recreate using steps above
```

**Issue: Permission denied errors**
```bash
# Check user permissions
docker exec gaming-marketing-mysql mysql -u root -p'123456' -e "
SELECT User, Host FROM mysql.user WHERE User = 'mcpuser';
SHOW GRANTS FOR 'mcpuser'@'%';
"

# Recreate user if needed
docker exec gaming-marketing-mysql mysql -u root -p'123456' -e "
DROP USER IF EXISTS 'mcpuser'@'%';
CREATE USER 'mcpuser'@'%' IDENTIFIED BY 'mcppassword';
GRANT ALL PRIVILEGES ON gaming_marketing.* TO 'mcpuser'@'%';
FLUSH PRIVILEGES;
"
```

**Issue: Data generation fails**
```bash
# Check table structure
docker exec gaming-marketing-mysql mysql -u mcpuser -p'mcppassword' gaming_marketing -e "SHOW CREATE TABLE campaigns;"

# Check for foreign key constraints
docker exec gaming-marketing-mysql mysql -u mcpuser -p'mcppassword' gaming_marketing -e "
SELECT 
  TABLE_NAME,
  COLUMN_NAME,
  CONSTRAINT_NAME,
  REFERENCED_TABLE_NAME,
  REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE REFERENCED_TABLE_SCHEMA = 'gaming_marketing';
"
```

#### 10. Cleanup and Reset

**To start completely fresh**:
```bash
# Stop and remove container
docker stop gaming-marketing-mysql
docker rm gaming-marketing-mysql

# Remove any volumes (if using docker-compose)
docker-compose down -v

# Remove Docker images (optional)
docker rmi mysql:8.0
```

**To reset data only (keep container)**:
```bash
# Drop and recreate database
docker exec gaming-marketing-mysql mysql -u root -p'123456' -e "
DROP DATABASE IF EXISTS gaming_marketing;
CREATE DATABASE gaming_marketing;
GRANT ALL PRIVILEGES ON gaming_marketing.* TO 'mcpuser'@'%';
FLUSH PRIVILEGES;
"

# Then rerun schema creation and data generation
```

### Quick Start Summary

For experienced users, here's the condensed version:

```bash
# 1. Start container
docker-compose up -d

# 2. Create schema
MYSQL_HOST=localhost MYSQL_USER=mcpuser MYSQL_PASSWORD=mcppassword MYSQL_DATABASE=gaming_marketing python setup_in_gaming_marketing.py

# 3. Generate data
MYSQL_HOST=localhost MYSQL_USER=mcpuser MYSQL_PASSWORD=mcppassword MYSQL_DATABASE=gaming_marketing python data_generator_high_volume.py

# 4. Verify
docker exec gaming-marketing-mysql mysql -u mcpuser -p'mcppassword' gaming_marketing -e "SELECT COUNT(*) as total_rows FROM (SELECT 1 FROM games UNION ALL SELECT 1 FROM campaigns UNION ALL SELECT 1 FROM ad_creatives UNION ALL SELECT 1 FROM user_sessions UNION ALL SELECT 1 FROM in_game_events UNION ALL SELECT 1 FROM ad_performance UNION ALL SELECT 1 FROM purchase_events) t;"
## Sample Queries

### Marketing Performance Analysis

```sql
-- Campaign performance overview
SELECT 
    c.campaign_name,
    g.game_name,
    p.platform_name,
    SUM(ap.impressions) AS total_impressions,
    SUM(ap.clicks) AS total_clicks,
    SUM(ap.installs) AS total_installs,
    SUM(ap.spend) AS total_spend,
    AVG(ap.ctr) AS avg_ctr,
    AVG(ap.cpi) AS avg_cpi,
    AVG(ap.roas) AS avg_roas
FROM 
    campaigns c
JOIN 
    games g ON c.game_id = g.game_id
JOIN 
    ad_platforms p ON c.platform_id = p.platform_id
JOIN 
    ad_performance ap ON c.campaign_id = ap.campaign_id
GROUP BY 
    c.campaign_id, g.game_id, p.platform_id
ORDER BY 
    total_installs DESC;
```

### User Behavior Analysis

```sql
-- User progression analysis
SELECT 
    g.game_name,
    pe.level_id,
    pe.event_type,
    COUNT(*) AS event_count,
    AVG(pe.time_spent) AS avg_time_spent,
    AVG(pe.attempts) AS avg_attempts
FROM 
    progression_events pe
JOIN 
    games g ON pe.game_id = g.game_id
GROUP BY 
    g.game_id, pe.level_id, pe.event_type
ORDER BY 
    g.game_name, pe.level_id;
```

### Revenue Analysis

```sql
-- Purchase analysis by game
SELECT 
    g.game_name,
    pu.product_type,
    COUNT(*) AS purchase_count,
    SUM(pu.price) AS total_revenue,
    AVG(pu.price) AS avg_purchase_value,
    COUNT(DISTINCT pu.user_id) AS unique_paying_users
FROM 
    purchase_events pu
JOIN 
    games g ON pu.game_id = g.game_id
GROUP BY 
    g.game_id, pu.product_type
ORDER BY 
    total_revenue DESC;
```

### Session and Event Analysis

```sql
-- Daily active users and session metrics
SELECT 
    DATE(us.session_start) as session_date,
    g.game_name,
    COUNT(DISTINCT us.user_id) as daily_active_users,
    COUNT(us.session_id) as total_sessions,
    AVG(us.session_duration) as avg_session_duration,
    SUM(us.session_duration) as total_playtime
FROM 
    user_sessions us
JOIN 
    games g ON us.game_id = g.game_id
WHERE 
    us.session_start >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY 
    DATE(us.session_start), g.game_id
ORDER BY 
    session_date DESC, daily_active_users DESC;
```

### Ad Performance by Creative Type

```sql
-- Creative performance comparison
SELECT 
    ac.creative_type,
    COUNT(DISTINCT ac.creative_id) as creative_count,
    SUM(ap.impressions) as total_impressions,
    SUM(ap.clicks) as total_clicks,
    SUM(ap.installs) as total_installs,
    SUM(ap.spend) as total_spend,
    AVG(ap.ctr) as avg_ctr,
    AVG(ap.cpi) as avg_cpi,
    AVG(ap.roas) as avg_roas
FROM 
    ad_creatives ac
JOIN 
    ad_performance ap ON ac.creative_id = ap.creative_id
GROUP BY 
    ac.creative_type
ORDER BY 
    total_installs DESC;
```

## Files in this Directory

### Core Setup Files
- **gaming_marketing_schema.sql**: Complete SQL schema for creating all tables
- **setup_in_gaming_marketing.py**: Script to create tables in gaming_marketing database
- **docker-compose.yml**: Docker Compose configuration for MySQL container
- **.env.docker**: Environment variables for Docker setup

### Data Generation Scripts
- **data_generator_high_volume.py**: High-volume data generator (80k+ rows) - **Recommended**
- **data_generator_gaming_marketing.py**: Small sample data generator (~230 rows)
- **generate_remaining_data.py**: Helper script for completing partial data generation
- **verify_data.py**: Script to verify the generated data

### Configuration Files
- **requirements-data-gen.txt**: Python dependencies for data generation
- **.env**: Environment variables file template
- **setup_env.sh**: Script to set environment variables

### Documentation
- **DATA_DICTIONARY.md**: Detailed description of all tables and fields
- **README.md**: This comprehensive setup guide

### Helper Scripts
- **cleanup_launcher.py**: Database cleanup utilities
- **test_mysql_permissions.py**: Permission testing script
- **create_database_and_permissions.py**: Database and user setup script

## Data Dictionary

See the [DATA_DICTIONARY.md](DATA_DICTIONARY.md) file for a complete description of all tables and fields.

## Performance Considerations

With 80k+ rows of data, consider these optimizations:

### Indexing
The schema includes optimized indexes for common query patterns:
- Campaign performance queries
- User behavior analysis
- Time-based filtering
- Cross-table joins

### Query Optimization Tips
```sql
-- Use date ranges for better performance
WHERE session_start >= '2024-01-01' AND session_start < '2024-02-01'

-- Limit results for large datasets
SELECT * FROM in_game_events ORDER BY event_timestamp DESC LIMIT 1000;

-- Use aggregation for summary reports
SELECT DATE(session_start), COUNT(*) FROM user_sessions GROUP BY DATE(session_start);
```

### Monitoring
```sql
-- Check table sizes
SELECT 
    table_name,
    table_rows,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM 
    information_schema.tables 
WHERE 
    table_schema = 'gaming_marketing'
ORDER BY 
    table_rows DESC;
```

## Next Steps

After setting up the database with 80k+ rows, you can:

1. **Build Analytics Dashboards**: Use tools like Grafana, Tableau, or custom web apps
2. **Implement Real-time Processing**: Set up streaming data pipelines
3. **Add Machine Learning**: Train models for user behavior prediction or campaign optimization
4. **Scale Testing**: Test database performance under various load conditions
5. **Extend Schema**: Add more tables for advanced analytics needs

## Support

If you encounter issues during setup:

1. Check the troubleshooting section above
2. Verify Docker and Python installations
3. Ensure port 3306 is available
4. Review container logs: `docker logs gaming-marketing-mysql`
5. Test database connectivity step by step

The database is designed to be production-ready and can handle realistic gaming marketing analytics workloads.
