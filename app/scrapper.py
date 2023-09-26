# -*- coding: utf-8 -*-
"""

Scrapper to put text files from https://download.bls.gov/pub/time.series/ce/ in an existing PostgreSQL database in localhost:5432 called 'employee_case'

Only the following files will be downloaded:
    ce.data.0.ALLCESSeries
    ce.data.01a.CurrentSeasAE
    ce.data.02b.AllRealEarningsAE
    ce.data.03c.AllRealEarningsPE
    ce.data.Goog
    ce.datatype
    ce.footnote
    ce.industry
    ce.period
    ce.seasonal
    ce.series
    ce.supersector

Based on the documentation found in https://download.bls.gov/pub/time.series/ce/ce.txt these will serve the intended purposes of analyzing:
    1. Women government employment trend
    2. Production vs Supervision employment trend

"""

import requests
import psycopg2
import re
from io import StringIO

# URL for the text files
url = "https://download.bls.gov/pub/time.series/ce/"

# Database connection parameters
db_params = {
    "database": "employee_case",
    "user": "nim_grav",
    "password": "nimble_grtavity_usecase",
    "host": "localhost",  
    "port": "5432",       
}

# Connect to employee_case database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Function to download and load data into the database
def download_and_load_file(filename):
    file_url = url + filename
    # A modification to the agent is necesary to avoid 403 response from website
    response = requests.get(file_url,
                            headers = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'})
    if response.status_code == 200:
        # Read the content of the file
        file_content = response.text
        
        # Read and transform first line for columns names
        first_line_num = file_content.splitlines()[0]
        first_line_num = re.sub(r'\t', ' TEXT,', first_line_num)
        first_line_num = first_line_num + ' TEXT'
        
        # Create a temporary table for data insertion
        cursor.execute(f"DROP TABLE IF EXISTS temp_table;")
        cursor.execute(f"CREATE TEMP TABLE temp_table ({first_line_num});")
        
        # Copy data from the downloaded file into the temporary table
        data_to_insert = StringIO(file_content)
        cursor.copy_expert(f"COPY temp_table FROM stdin DELIMITER E'\\t' HEADER", data_to_insert)
        
        # Insert data from the temporary table into the target table
        table_name = filename.replace(".","_")
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        cursor.execute(f"CREATE TABLE {table_name} AS SELECT * FROM temp_table;")
        
        # Commit the transaction
        conn.commit()
        print(f"Data from {filename} loaded into the database.")
    else:
        print(f"Failed to download {filename}. Status code: {response.status_code}")

# List of files to download and load
files_to_download = [
    "ce.data.0.ALLCESSeries",
    "ce.data.01a.CurrentSeasAE",
    "ce.data.02b.AllRealEarningsAE",
    "ce.data.03c.AllRealEarningsPE",
    "ce.data.Goog",
    "ce.datatype",
    "ce.footnote",
    "ce.industry",
    "ce.period",
    "ce.seasonal",
    "ce.series",
    "ce.supersector"
]

# Loop through the list of files and load data into the database
for filename in files_to_download:
    download_and_load_file(filename)
    
# Execute the SQL scripts
with open("MatViz_generate.sql", "r") as sql_file:
    sql_script = sql_file.read()
    cursor.execute(sql_script)
    conn.commit()


with open("RestApi_setup.sql", "r") as sql_file:
    sql_script = sql_file.read()
    cursor.execute(sql_script)
    conn.commit()

# Close the database connection
cursor.close()
conn.close()