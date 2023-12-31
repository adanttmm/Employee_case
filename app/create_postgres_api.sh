#!/bin/bash

# Start the PostgreSQL service
sudo service postgresql start

# Create a new PostgreSQL database
echo "Creating a new database employee_casse to load scrapped data..."
sudo -u postgres createdb employee_case

# Create a new PostgreSQL user with a password
echo "Creating a new user nim_grav to manipulate DB..."
sudo -u postgres psql -c "CREATE USER nim_grav WITH PASSWORD 'nimble_grtavity_usecase';"

# Grant privileges to the new user on the database
echo "Granting privileges..."
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE employee_case TO nim_grav;"

# Create schema for API
echo "Creating API schema..."
sudo -u postgres psql -c "CREATE SCHEMA emp_api;"

# Create API role
echo "Creating API role..."
sudo -u postgres psql -c "CREATE ROLE web_anon nologin;"
sudo -u postgres psql -c "GRANT web_anon TO nim_grav;"

# Stop the PostgreSQL service
sudo service postgresql stop

echo "PosgreSQL employee_case database with nim_grav user and PostgREST ready to use."




