-- Gaming Marketing Database Schema
-- Run this with: mysql -h localhost -P 3306 -u mcpuser -pmcppassword < gaming_marketing_schema.sql

-- Create database
CREATE DATABASE IF NOT EXISTS mcpdb;
USE mcpdb;

-- Drop tables if they exist to start fresh
DROP TABLE IF EXISTS user_segment_memberships;
DROP TABLE IF EXISTS user_segments;
DROP TABLE IF EXISTS error_events;
DROP TABLE IF EXISTS feature_usage_events;
DROP TABLE IF EXISTS attribution_events;
DROP TABLE IF EXISTS social_events;
DROP TABLE IF EXISTS progression_events;
DROP TABLE IF EXISTS purchase_events;
DROP TABLE IF EXISTS ad_engagement_events;
DROP TABLE IF EXISTS in_game_events;
DROP TABLE IF EXISTS user_sessions;
DROP TABLE IF EXISTS cohort_analysis;
DROP TABLE IF EXISTS ad_network_revenue;
DROP TABLE IF EXISTS monetization;
DROP TABLE IF EXISTS user_retention;
DROP TABLE IF EXISTS user_acquisition;
DROP TABLE IF EXISTS ad_performance;
DROP TABLE IF EXISTS ad_creatives;
DROP TABLE IF EXISTS campaigns;
DROP TABLE IF EXISTS ad_platforms;
DROP TABLE IF EXISTS games;

-- Create games table
CREATE TABLE games (
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    game_name VARCHAR(100) NOT NULL,
    genre VARCHAR(50) NOT NULL,
    release_date DATE NOT NULL,
    platform_type VARCHAR(50) NOT NULL,
    developer VARCHAR(100) NOT NULL,
    publisher VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create ad platforms table
CREATE TABLE ad_platforms (
    platform_id INT AUTO_INCREMENT PRIMARY KEY,
    platform_name VARCHAR(50) NOT NULL,
    platform_type VARCHAR(50) NOT NULL,
    api_credentials VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create campaigns table
CREATE TABLE campaigns (
    campaign_id INT AUTO_INCREMENT PRIMARY KEY,
    campaign_name VARCHAR(100) NOT NULL,
    game_id INT NOT NULL,
    platform_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    budget DECIMAL(15, 2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    objective VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (platform_id) REFERENCES ad_platforms(platform_id)
);

-- Create ad creatives table
CREATE TABLE ad_creatives (
    creative_id INT AUTO_INCREMENT PRIMARY KEY,
    campaign_id INT NOT NULL,
    creative_name VARCHAR(100) NOT NULL,
    creative_type VARCHAR(50) NOT NULL,
    creative_url VARCHAR(255) NOT NULL,
    dimensions VARCHAR(20),
    duration INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id)
);

-- Create ad performance table
CREATE TABLE ad_performance (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,
    campaign_id INT NOT NULL,
    creative_id INT NOT NULL,
    platform_id INT NOT NULL,
    date DATE NOT NULL,
    impressions INT NOT NULL DEFAULT 0,
    clicks INT NOT NULL DEFAULT 0,
    installs INT NOT NULL DEFAULT 0,
    spend DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    ctr DECIMAL(10, 4),
    cpi DECIMAL(10, 2),
    roas DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id),
    FOREIGN KEY (creative_id) REFERENCES ad_creatives(creative_id),
    FOREIGN KEY (platform_id) REFERENCES ad_platforms(platform_id)
);

-- Create user acquisition table
CREATE TABLE user_acquisition (
    acquisition_id INT AUTO_INCREMENT PRIMARY KEY,
    campaign_id INT NOT NULL,
    platform_id INT NOT NULL,
    date DATE NOT NULL,
    country VARCHAR(2) NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    os_version VARCHAR(20) NOT NULL,
    installs INT NOT NULL DEFAULT 0,
    cost DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    ltv_prediction DECIMAL(15, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id),
    FOREIGN KEY (platform_id) REFERENCES ad_platforms(platform_id)
);

-- Create user retention table
CREATE TABLE user_retention (
    retention_id INT AUTO_INCREMENT PRIMARY KEY,
    acquisition_id INT NOT NULL,
    day_number INT NOT NULL,
    retention_rate DECIMAL(5, 2) NOT NULL,
    sessions INT NOT NULL DEFAULT 0,
    session_duration INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (acquisition_id) REFERENCES user_acquisition(acquisition_id)
);

-- Create monetization table
CREATE TABLE monetization (
    monetization_id INT AUTO_INCREMENT PRIMARY KEY,
    acquisition_id INT NOT NULL,
    date DATE NOT NULL,
    revenue_type VARCHAR(20) NOT NULL,
    revenue_amount DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    transactions INT NOT NULL DEFAULT 0,
    arpu DECIMAL(10, 4),
    arppu DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (acquisition_id) REFERENCES user_acquisition(acquisition_id)
);

-- Create ad network revenue table
CREATE TABLE ad_network_revenue (
    revenue_id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL,
    platform_id INT NOT NULL,
    date DATE NOT NULL,
    ad_format VARCHAR(20) NOT NULL,
    impressions INT NOT NULL DEFAULT 0,
    revenue DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    ecpm DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (platform_id) REFERENCES ad_platforms(platform_id)
);

-- Create cohort analysis table
CREATE TABLE cohort_analysis (
    cohort_id INT AUTO_INCREMENT PRIMARY KEY,
    acquisition_id INT NOT NULL,
    cohort_date DATE NOT NULL,
    day_number INT NOT NULL,
    retention_rate DECIMAL(5, 2) NOT NULL,
    revenue DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    arpu DECIMAL(10, 4),
    roas DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (acquisition_id) REFERENCES user_acquisition(acquisition_id)
);

-- Create user sessions table
CREATE TABLE user_sessions (
    session_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    game_id INT NOT NULL,
    session_start TIMESTAMP NOT NULL,
    session_end TIMESTAMP,
    session_duration INT,
    device_type VARCHAR(50) NOT NULL,
    os_version VARCHAR(20) NOT NULL,
    country VARCHAR(2) NOT NULL,
    acquisition_source VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);

-- Create in-game events table
CREATE TABLE in_game_events (
    event_id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    game_id INT NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    level_id VARCHAR(50),
    event_value DECIMAL(15, 2),
    event_details JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES user_sessions(session_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);

-- Create ad engagement events table
CREATE TABLE ad_engagement_events (
    ad_event_id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    game_id INT NOT NULL,
    ad_unit_id VARCHAR(50) NOT NULL,
    ad_network VARCHAR(50) NOT NULL,
    ad_type VARCHAR(20) NOT NULL,
    event_type VARCHAR(20) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    reward_amount INT,
    reward_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES user_sessions(session_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);

-- Create purchase events table
CREATE TABLE purchase_events (
    purchase_id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    game_id INT NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    product_type VARCHAR(20) NOT NULL,
    purchase_timestamp TIMESTAMP NOT NULL,
    currency VARCHAR(3) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    payment_provider VARCHAR(50) NOT NULL,
    transaction_id VARCHAR(100) NOT NULL,
    is_first_purchase BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES user_sessions(session_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);

-- Create progression events table
CREATE TABLE progression_events (
    progression_id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    game_id INT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    level_id VARCHAR(50) NOT NULL,
    event_type VARCHAR(20) NOT NULL,
    score INT,
    stars INT,
    time_spent INT NOT NULL,
    attempts INT NOT NULL DEFAULT 1,
    resources_used JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES user_sessions(session_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);

-- Create social events table
CREATE TABLE social_events (
    social_id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    game_id INT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    target_user_id VARCHAR(36),
    content_id VARCHAR(50),
    platform VARCHAR(50) NOT NULL,
    success BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES user_sessions(session_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);

-- Create attribution events table
CREATE TABLE attribution_events (
    attribution_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    install_timestamp TIMESTAMP NOT NULL,
    attribution_platform VARCHAR(50) NOT NULL,
    campaign_id INT,
    ad_group VARCHAR(100),
    creative_id INT,
    click_timestamp TIMESTAMP,
    impression_timestamp TIMESTAMP,
    install_source VARCHAR(50) NOT NULL,
    device_id VARCHAR(100) NOT NULL,
    ip_address VARCHAR(100),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id),
    FOREIGN KEY (creative_id) REFERENCES ad_creatives(creative_id)
);

-- Create feature usage events table
CREATE TABLE feature_usage_events (
    feature_event_id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    game_id INT NOT NULL,
    feature_id VARCHAR(50) NOT NULL,
    feature_name VARCHAR(100) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    time_spent INT NOT NULL,
    engagement_level INT NOT NULL,
    outcome VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES user_sessions(session_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);

-- Create error events table
CREATE TABLE error_events (
    error_id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    game_id INT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    error_type VARCHAR(50) NOT NULL,
    error_message TEXT NOT NULL,
    stack_trace TEXT,
    severity VARCHAR(20) NOT NULL,
    is_crash BOOLEAN NOT NULL DEFAULT FALSE,
    device_info JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES user_sessions(session_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);

-- Create user segments table
CREATE TABLE user_segments (
    segment_id INT AUTO_INCREMENT PRIMARY KEY,
    segment_name VARCHAR(100) NOT NULL,
    segment_description TEXT,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    segment_criteria JSON NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create user segment memberships table
CREATE TABLE user_segment_memberships (
    membership_id INT AUTO_INCREMENT PRIMARY KEY,
    segment_id INT NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    join_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    exit_date TIMESTAMP NULL,
    source VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (segment_id) REFERENCES user_segments(segment_id)
);

-- Create indexes for better performance
CREATE INDEX idx_campaigns_game ON campaigns(game_id);
CREATE INDEX idx_campaigns_platform ON campaigns(platform_id);
CREATE INDEX idx_ad_creatives_campaign ON ad_creatives(campaign_id);
CREATE INDEX idx_ad_performance_date ON ad_performance(date);
CREATE INDEX idx_ad_performance_campaign ON ad_performance(campaign_id);
CREATE INDEX idx_user_acquisition_date ON user_acquisition(date);
CREATE INDEX idx_user_acquisition_country ON user_acquisition(country);
CREATE INDEX idx_user_retention_day ON user_retention(day_number);
CREATE INDEX idx_monetization_date ON monetization(date);
CREATE INDEX idx_monetization_type ON monetization(revenue_type);
CREATE INDEX idx_ad_network_revenue_date ON ad_network_revenue(date);
CREATE INDEX idx_cohort_analysis_date ON cohort_analysis(cohort_date);
CREATE INDEX idx_user_sessions_user ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_game ON user_sessions(game_id);
CREATE INDEX idx_user_sessions_start ON user_sessions(session_start);
CREATE INDEX idx_in_game_events_user ON in_game_events(user_id);
CREATE INDEX idx_in_game_events_type ON in_game_events(event_type);
CREATE INDEX idx_in_game_events_timestamp ON in_game_events(event_timestamp);
CREATE INDEX idx_ad_engagement_events_user ON ad_engagement_events(user_id);
CREATE INDEX idx_ad_engagement_events_type ON ad_engagement_events(event_type);
CREATE INDEX idx_purchase_events_user ON purchase_events(user_id);
CREATE INDEX idx_purchase_events_timestamp ON purchase_events(purchase_timestamp);
CREATE INDEX idx_progression_events_user ON progression_events(user_id);
CREATE INDEX idx_progression_events_level ON progression_events(level_id);
CREATE INDEX idx_social_events_user ON social_events(user_id);
CREATE INDEX idx_attribution_events_user ON attribution_events(user_id);
CREATE INDEX idx_feature_usage_events_feature ON feature_usage_events(feature_id);
CREATE INDEX idx_error_events_type ON error_events(error_type);
CREATE INDEX idx_user_segment_memberships_user ON user_segment_memberships(user_id);

-- Insert sample data for games
INSERT INTO games (game_name, genre, release_date, platform_type, developer, publisher) VALUES
('Puzzle Quest', 'Puzzle', '2023-01-15', 'Mobile', 'GameStudio A', 'Publisher X'),
('Epic RPG Adventure', 'RPG', '2022-05-20', 'Mobile', 'GameStudio B', 'Publisher Y'),
('Strategy Masters', 'Strategy', '2023-03-10', 'Mobile', 'GameStudio C', 'Publisher Z'),
('Casual Tycoon', 'Simulation', '2022-11-05', 'Mobile', 'GameStudio D', 'Publisher X'),
('Battle Royale Heroes', 'Action', '2023-02-28', 'Mobile', 'GameStudio E', 'Publisher Y');

-- Insert sample data for ad platforms
INSERT INTO ad_platforms (platform_name, platform_type, api_credentials) VALUES
('Facebook', 'Social', 'facebook_api_credentials'),
('Google Ads', 'Search', 'google_api_credentials'),
('AppLovin', 'Ad Network', 'applovin_api_credentials'),
('TikTok', 'Social', 'tiktok_api_credentials'),
('Unity Ads', 'Ad Network', 'unity_api_credentials'),
('ironSource', 'Ad Network', 'ironsource_api_credentials'),
('Snapchat', 'Social', 'snapchat_api_credentials'),
('Apple Search Ads', 'Search', 'apple_api_credentials');

-- Show the tables created
SHOW TABLES;
