import csv
import uuid
import random
from datetime import datetime, timedelta, timezone
import numpy as np

def create_sample_data():
    """
    Generates 100,000 sample data records and saves them to a CSV file
    based on the requirements in the README.md file.
    """
    # --- Constants from README ---
    FILE_NAME = "sample_data.csv"
    NUM_RECORDS = 100000
    DATE_STR = "2025-01-01"
    MIN_TIME_STR = "00:08:00Z+0900"
    MAX_TIME_STR = "21:00:00Z+0900"
    # --- End of Constants from README ---
    
    # --- Data Generation Parameters ---
    # Age distribution parameters
    AGE_DF = 20
    AGE_MAX = 100
    
    MAX_INTERVAL_MINUTES = 45
    
    # Age distribution parameters
    AGE_DF = 20
    AGE_MAX = 100

    # Interval distribution parameters
    INTERVAL_DF = 10

    GENDERS = ["male", "female"]
    
    # --- Timezone and Timestamp Setup ---
    JST = timezone(timedelta(hours=9))
    
    start_datetime = datetime.strptime(f"{DATE_STR}T{MIN_TIME_STR}")
    end_datetime = datetime.strptime(f"{DATE_STR}T{MAX_TIME_STR}")

    # To ensure exit_timestamp does not exceed MAX_TIME, the latest enter_timestamp
    # must be MAX_TIME - MAX_INTERVAL.
    max_enter_datetime = end_datetime - timedelta(minutes=MAX_INTERVAL_MINUTES)
    
    # --- Data Generation ---
    with open(FILE_NAME, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(["id", "enter_timestamp", "exit_timestamp", "age", "gender"])
        
        for _ in range(NUM_RECORDS):
            # Generate enter_timestamp
            random_timestamp = random.uniform(start_datetime.timestamp(), end_datetime.timestamp())
            enter_dt = datetime.fromtimestamp(random_timestamp, tz=JST)
            
            # Generate interval and exit_timestamp
            while True:
                interval_minutes = np.random.chisquare(df=INTERVAL_DF)
                if interval_minutes <= MAX_INTERVAL_MINUTES:
                    exit_dt = enter_dt + timedelta(minutes=interval_minutes)
                    if exit_dt <= max_enter_datetime :
                    break
            interval_minutes = min(np.random.chisquare(df=INTERVAL_DF), MAX_INTERVAL_MINUTES)
            exit_dt = enter_dt + timedelta(minutes=interval_minutes)

            # Format timestamps to the required string format
            enter_str = enter_dt.strftime('%Y-%m-%dT%H:%M:%SZ+0900')
            exit_str = exit_dt.strftime('%Y-%m-%dT%H:%M:%SZ+0900')

            # Generate age
            # The age follows a chi-squared distribution and is capped at AGE_MAX.
            age = min(int(np.random.chisquare(df=AGE_DF)), AGE_MAX)
            
            # Generate gender
            gender = random.choice(GENDERS)
            
            # Generate ID
            id_str = str(uuid.uuid4())
            
            # Write row to CSV
            writer.writerow([id_str, enter_str, exit_str, age, gender])

    print(f"Successfully generated {NUM_RECORDS} records in '{FILE_NAME}'")

if __name__ == "__main__":
    create_sample_data()