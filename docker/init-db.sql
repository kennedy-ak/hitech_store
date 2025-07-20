-- Initialize HiTech Clan Technology Solutions Database
-- This script runs automatically when the PostgreSQL container starts

-- Create database if it doesn't exist
-- (Not needed as Docker creates it from POSTGRES_DB env var)

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON DATABASE hitech_store TO hitech_user;

-- Set timezone
SET timezone = 'UTC';