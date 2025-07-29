#!/bin/bash
# Setup environment variables for gaming marketing database

export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=mcpuser
export MYSQL_PASSWORD=mcppassword
export MYSQL_DATABASE=gaming_marketing

echo "Environment variables set:"
echo "MYSQL_HOST: $MYSQL_HOST"
echo "MYSQL_PORT: $MYSQL_PORT"
echo "MYSQL_USER: $MYSQL_USER"
echo "MYSQL_DATABASE: $MYSQL_DATABASE"
echo "MYSQL_PASSWORD: [HIDDEN]"
echo ""
echo "To use these variables in your current shell session, run:"
echo "source setup_env.sh"
