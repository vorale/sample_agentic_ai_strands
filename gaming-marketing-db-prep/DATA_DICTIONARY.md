# Gaming Marketing Database - Data Dictionary

## Aggregated Marketing Data Tables

### games
Stores information about the games being marketed.

| Column | Type | Description |
|--------|------|-------------|
| game_id | INT | Primary key |
| game_name | VARCHAR(100) | Name of the game |
| genre | VARCHAR(50) | Game genre (Puzzle, RPG, etc.) |
| release_date | DATE | When the game was released |
| platform_type | VARCHAR(50) | Mobile, Console, PC, etc. |
| developer | VARCHAR(100) | Game developer name |
| publisher | VARCHAR(100) | Game publisher name |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Record update timestamp |

### ad_platforms
Stores information about advertising platforms.

| Column | Type | Description |
|--------|------|-------------|
| platform_id | INT | Primary key |
| platform_name | VARCHAR(50) | Platform name (Facebook, Google, etc.) |
| platform_type | VARCHAR(50) | Platform type (Social, Search, etc.) |
| api_credentials | VARCHAR(255) | Reference to API credentials |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Record update timestamp |

### campaigns
Stores information about marketing campaigns.

| Column | Type | Description |
|--------|------|-------------|
| campaign_id | INT | Primary key |
| campaign_name | VARCHAR(100) | Name of the campaign |
| game_id | INT | Foreign key to games table |
| platform_id | INT | Foreign key to ad_platforms table |
| start_date | DATE | Campaign start date |
| end_date | DATE | Campaign end date (NULL if ongoing) |
| budget | DECIMAL(15,2) | Total campaign budget |
| status | VARCHAR(20) | Active, Paused, or Completed |
| objective | VARCHAR(50) | Campaign objective |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Record update timestamp |

### ad_creatives
Stores information about ad creatives used in campaigns.

| Column | Type | Description |
|--------|------|-------------|
| creative_id | INT | Primary key |
| campaign_id | INT | Foreign key to campaigns table |
| creative_name | VARCHAR(100) | Name of the creative |
| creative_type | VARCHAR(50) | Type of creative (Video, Image, etc.) |
| creative_url | VARCHAR(255) | URL to the creative asset |
| dimensions | VARCHAR(20) | Dimensions of the creative |
| duration | INT | Duration for video creatives (seconds) |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Record update timestamp |

### ad_performance
Stores daily performance metrics for ads.

| Column | Type | Description |
|--------|------|-------------|
| performance_id | INT | Primary key |
| campaign_id | INT | Foreign key to campaigns table |
| creative_id | INT | Foreign key to ad_creatives table |
| platform_id | INT | Foreign key to ad_platforms table |
| date | DATE | Date of the metrics |
| impressions | INT | Number of ad impressions |
| clicks | INT | Number of clicks |
| installs | INT | Number of app installs |
| spend | DECIMAL(15,2) | Amount spent |
| ctr | DECIMAL(10,4) | Click-through rate |
| cpi | DECIMAL(10,2) | Cost per install |
| roas | DECIMAL(10,2) | Return on ad spend |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Record update timestamp |

### user_acquisition
Stores user acquisition data by campaign, country, and device.

| Column | Type | Description |
|--------|------|-------------|
| acquisition_id | INT | Primary key |
| campaign_id | INT | Foreign key to campaigns table |
| platform_id | INT | Foreign key to ad_platforms table |
| date | DATE | Date of acquisition |
| country | VARCHAR(2) | User's country (ISO code) |
| device_type | VARCHAR(50) | User's device type |
| os_version | VARCHAR(20) | User's OS version |
| installs | INT | Number of installs |
| cost | DECIMAL(15,2) | Cost of acquisition |
| ltv_prediction | DECIMAL(15,2) | Predicted lifetime value |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Record update timestamp |

### user_retention
Stores retention metrics for acquired users.

| Column | Type | Description |
|--------|------|-------------|
| retention_id | INT | Primary key |
| acquisition_id | INT | Foreign key to user_acquisition table |
| day_number | INT | Retention day (1, 3, 7, 14, 30) |
| retention_rate | DECIMAL(5,2) | Percentage of users retained |
| sessions | INT | Number of sessions |
| session_duration | INT | Average session duration (seconds) |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Record update timestamp |

### monetization
Stores monetization data for acquired users.

| Column | Type | Description |
|--------|------|-------------|
| monetization_id | INT | Primary key |
| acquisition_id | INT | Foreign key to user_acquisition table |
| date | DATE | Date of revenue |
| revenue_type | VARCHAR(20) | IAP, Subscription, Ad revenue |
| revenue_amount | DECIMAL(15,2) | Amount of revenue |
| transactions | INT | Number of transactions |
| arpu | DECIMAL(10,4) | Average revenue per user |
| arppu | DECIMAL(10,2) | Average revenue per paying user |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Record update timestamp |

### ad_network_revenue
Stores revenue from ad networks.

| Column | Type | Description |
|--------|------|-------------|
| revenue_id | INT | Primary key |
| game_id | INT | Foreign key to games table |
| platform_id | INT | Foreign key to ad_platforms table |
| date | DATE | Date of revenue |
| ad_format | VARCHAR(20) | Ad format (interstitial, rewarded, etc.) |
| impressions | INT | Number of ad impressions |
| revenue | DECIMAL(15,2) | Revenue generated |
| ecpm | DECIMAL(10,2) | Effective cost per mille |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Record update timestamp |

### cohort_analysis
Stores cohort analysis data.

| Column | Type | Description |
|--------|------|-------------|
| cohort_id | INT | Primary key |
| acquisition_id | INT | Foreign key to user_acquisition table |
| cohort_date | DATE | Date of the cohort |
| day_number | INT | Day since acquisition |
| retention_rate | DECIMAL(5,2) | Retention rate for this day |
| revenue | DECIMAL(15,2) | Revenue for this day |
| arpu | DECIMAL(10,4) | ARPU for this day |
| roas | DECIMAL(10,2) | ROAS for this day |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Record update timestamp |

## Event Telemetry Tables

### user_sessions
Stores individual user session data.

| Column | Type | Description |
|--------|------|-------------|
| session_id | VARCHAR(36) | Primary key (UUID) |
| user_id | VARCHAR(36) | User identifier (UUID) |
| game_id | INT | Foreign key to games table |
| session_start | TIMESTAMP | When session started |
| session_end | TIMESTAMP | When session ended (NULL if ongoing) |
| session_duration | INT | Duration in seconds |
| device_type | VARCHAR(50) | User's device |
| os_version | VARCHAR(20) | Operating system version |
| country | VARCHAR(2) | User's country (ISO code) |
| acquisition_source | VARCHAR(50) | Where user was acquired from |
| created_at | TIMESTAMP | Record creation timestamp |

### in_game_events
Stores individual in-game events.

| Column | Type | Description |
|--------|------|-------------|
| event_id | VARCHAR(36) | Primary key (UUID) |
| session_id | VARCHAR(36) | Foreign key to user_sessions table |
| user_id | VARCHAR(36) | User identifier (UUID) |
| game_id | INT | Foreign key to games table |
| event_type | VARCHAR(50) | Type of event |
| event_timestamp | TIMESTAMP | When the event occurred |
| level_id | VARCHAR(50) | Game level identifier (if applicable) |
| event_value | DECIMAL(15,2) | Numerical value associated with event |
| event_details | JSON | Additional event parameters |
| created_at | TIMESTAMP | Record creation timestamp |

### ad_engagement_events
Stores individual ad engagement events.

| Column | Type | Description |
|--------|------|-------------|
| ad_event_id | VARCHAR(36) | Primary key (UUID) |
| session_id | VARCHAR(36) | Foreign key to user_sessions table |
| user_id | VARCHAR(36) | User identifier (UUID) |
| game_id | INT | Foreign key to games table |
| ad_unit_id | VARCHAR(50) | Identifier for the ad unit |
| ad_network | VARCHAR(50) | Ad network that served the ad |
| ad_type | VARCHAR(20) | Type of ad (rewarded, interstitial, etc.) |
| event_type | VARCHAR(20) | Impression, click, complete, skip |
| event_timestamp | TIMESTAMP | When the event occurred |
| reward_amount | INT | Amount of virtual currency rewarded |
| reward_type | VARCHAR(50) | Type of reward given |
| created_at | TIMESTAMP | Record creation timestamp |

### purchase_events
Stores individual purchase events.

| Column | Type | Description |
|--------|------|-------------|
| purchase_id | VARCHAR(36) | Primary key (UUID) |
| session_id | VARCHAR(36) | Foreign key to user_sessions table |
| user_id | VARCHAR(36) | User identifier (UUID) |
| game_id | INT | Foreign key to games table |
| product_id | VARCHAR(50) | Identifier for the purchased item |
| product_type | VARCHAR(20) | Type of product |
| purchase_timestamp | TIMESTAMP | When the purchase occurred |
| currency | VARCHAR(3) | Currency of transaction |
| price | DECIMAL(10,2) | Price paid |
| payment_provider | VARCHAR(50) | Payment provider used |
| transaction_id | VARCHAR(100) | Platform transaction identifier |
| is_first_purchase | BOOLEAN | Whether this is user's first purchase |
| created_at | TIMESTAMP | Record creation timestamp |

### progression_events
Stores individual progression events.

| Column | Type | Description |
|--------|------|-------------|
| progression_id | VARCHAR(36) | Primary key (UUID) |
| session_id | VARCHAR(36) | Foreign key to user_sessions table |
| user_id | VARCHAR(36) | User identifier (UUID) |
| game_id | INT | Foreign key to games table |
| event_timestamp | TIMESTAMP | When the event occurred |
| level_id | VARCHAR(50) | Level identifier |
| event_type | VARCHAR(20) | start, complete, fail |
| score | INT | Score achieved |
| stars | INT | Stars/rating achieved |
| time_spent | INT | Time spent on level (seconds) |
| attempts | INT | Number of attempts |
| resources_used | JSON | Resources used during level |
| created_at | TIMESTAMP | Record creation timestamp |

### social_events
Stores individual social interaction events.

| Column | Type | Description |
|--------|------|-------------|
| social_id | VARCHAR(36) | Primary key (UUID) |
| session_id | VARCHAR(36) | Foreign key to user_sessions table |
| user_id | VARCHAR(36) | User identifier (UUID) |
| game_id | INT | Foreign key to games table |
| event_timestamp | TIMESTAMP | When the event occurred |
| event_type | VARCHAR(50) | invite_sent, invite_accepted, etc. |
| target_user_id | VARCHAR(36) | Recipient user identifier |
| content_id | VARCHAR(50) | Identifier for shared content |
| platform | VARCHAR(50) | Social platform used |
| success | BOOLEAN | Whether the social action was successful |
| created_at | TIMESTAMP | Record creation timestamp |

### attribution_events
Stores individual user attribution events.

| Column | Type | Description |
|--------|------|-------------|
| attribution_id | VARCHAR(36) | Primary key (UUID) |
| user_id | VARCHAR(36) | User identifier (UUID) |
| install_timestamp | TIMESTAMP | When the app was installed |
| attribution_platform | VARCHAR(50) | Attribution provider |
| campaign_id | INT | Foreign key to campaigns table |
| ad_group | VARCHAR(100) | Ad group identifier |
| creative_id | INT | Foreign key to ad_creatives table |
| click_timestamp | TIMESTAMP | When the ad was clicked |
| impression_timestamp | TIMESTAMP | When the ad was viewed |
| install_source | VARCHAR(50) | Source of install |
| device_id | VARCHAR(100) | Device identifier |
| ip_address | VARCHAR(100) | IP address (hashed/anonymized) |
| user_agent | TEXT | User agent string |
| created_at | TIMESTAMP | Record creation timestamp |

### feature_usage_events
Stores individual feature usage events.

| Column | Type | Description |
|--------|------|-------------|
| feature_event_id | VARCHAR(36) | Primary key (UUID) |
| session_id | VARCHAR(36) | Foreign key to user_sessions table |
| user_id | VARCHAR(36) | User identifier (UUID) |
| game_id | INT | Foreign key to games table |
| feature_id | VARCHAR(50) | Identifier for the game feature |
| feature_name | VARCHAR(100) | Name of the feature |
| event_timestamp | TIMESTAMP | When the feature was used |
| time_spent | INT | Time spent using the feature (seconds) |
| engagement_level | INT | Measure of engagement (1-10) |
| outcome | VARCHAR(50) | Result of feature usage |
| created_at | TIMESTAMP | Record creation timestamp |

### error_events
Stores individual error events.

| Column | Type | Description |
|--------|------|-------------|
| error_id | VARCHAR(36) | Primary key (UUID) |
| session_id | VARCHAR(36) | Foreign key to user_sessions table |
| user_id | VARCHAR(36) | User identifier (UUID) |
| game_id | INT | Foreign key to games table |
| event_timestamp | TIMESTAMP | When the error occurred |
| error_type | VARCHAR(50) | Type of error |
| error_message | TEXT | Error message |
| stack_trace | TEXT | Stack trace (if available) |
| severity | VARCHAR(20) | Error severity |
| is_crash | BOOLEAN | Whether the error caused a crash |
| device_info | JSON | Device information |
| created_at | TIMESTAMP | Record creation timestamp |

### user_segments
Stores user segment definitions.

| Column | Type | Description |
|--------|------|-------------|
| segment_id | INT | Primary key |
| segment_name | VARCHAR(100) | Name of the segment |
| segment_description | TEXT | Description of the segment |
| creation_date | TIMESTAMP | When the segment was created |
| segment_criteria | JSON | Segmentation criteria |
| is_active | BOOLEAN | Whether the segment is active |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Record update timestamp |

### user_segment_memberships
Stores user membership in segments.

| Column | Type | Description |
|--------|------|-------------|
| membership_id | INT | Primary key |
| segment_id | INT | Foreign key to user_segments table |
| user_id | VARCHAR(36) | User identifier (UUID) |
| join_date | TIMESTAMP | When the user joined the segment |
| exit_date | TIMESTAMP | When the user left the segment |
| source | VARCHAR(20) | How the user was added (automatic, manual) |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Record update timestamp |
