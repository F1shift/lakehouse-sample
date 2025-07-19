import csv
import uuid
import os
import random
from datetime import datetime, timedelta, timezone
import numpy as np

def create_sample_data(filename) -> list[dict[str, any]]:
    """
    Generates 100,000 sample data records and saves them to a CSV file
    based on the requirements in the README.md file.
    """
    # --- Constants from README ---
    
    NUM_RECORDS = 100000
    DATE_STR = "2025-01-01"
    MIN_TIME_STR = "08:00:00+0900"
    MAX_TIME_STR = "21:00:00+0900"
    # --- End of Constants from README ---
    
    # --- Data Generation Parameters ---
    # Age distribution parameters
    AGE_DF = 20
    AGE_MAX = 100
    
    
    # Age distribution parameters
    AGE_DF = 20
    AGE_MAX = 100

    # Interval distribution parameters
    INTERVAL_DF = 10
    MAX_INTERVAL_MINUTES = 45

    GENDERS = ["male", "female"]
    
    # --- Timezone and Timestamp Setup ---
    JST = timezone(timedelta(hours=9))
    
    start_datetime = datetime.fromisoformat(f"{DATE_STR}T{MIN_TIME_STR}")
    end_datetime = datetime.fromisoformat(f"{DATE_STR}T{MAX_TIME_STR}")

    # To ensure exit_timestamp does not exceed MAX_TIME, the latest enter_timestamp
    # must be MAX_TIME - MAX_INTERVAL.
    max_enter_datetime = end_datetime - timedelta(minutes=MAX_INTERVAL_MINUTES)

    # --- Parameters for bimodal distribution of enter_timestamp ---
    std_dev_hours = 2
    std_dev_seconds = std_dev_hours * 3600

    peak1_dt = datetime.fromisoformat(f"{DATE_STR}T12:00:00+0900")
    peak2_dt = datetime.fromisoformat(f"{DATE_STR}T20:00:00+0900")

    peak1_ts = peak1_dt.timestamp()
    peak2_ts = peak2_dt.timestamp()

    start_ts = start_datetime.timestamp()
    max_enter_ts = max_enter_datetime.timestamp()
    
    # --- Data Generation ---
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(["id", "enter_timestamp", "exit_timestamp", "age", "gender"])
        
        for _ in range(NUM_RECORDS):
            # Generate enter_timestamp with two peaks (around noon and 20:00)
            peak_ts = random.choice([peak1_ts, peak2_ts])
            
            while True:
                random_timestamp = np.random.normal(loc=peak_ts, scale=std_dev_seconds)
                if start_ts <= random_timestamp <= max_enter_ts:
                    break
            
            enter_dt = datetime.fromtimestamp(random_timestamp, tz=JST)
            
            # Generate interval and exit_timestamp
            while True:
                interval_minutes = np.random.chisquare(df=INTERVAL_DF)
                if interval_minutes <= MAX_INTERVAL_MINUTES:
                    break
            exit_dt = enter_dt + timedelta(minutes=interval_minutes)

            # Format timestamps to the required string format
            enter_str = enter_dt.isoformat()
            exit_str = exit_dt.isoformat()

            # Generate age
            # The age follows a chi-squared distribution and is capped at AGE_MAX.
            while True:
                age = int(np.random.chisquare(df=AGE_DF))
                if age <= AGE_MAX:
                    break
            
            # Generate gender
            gender = random.choice(GENDERS)
            
            # Generate ID
            id_str = str(uuid.uuid4())
            
            # Write row to CSV
            writer.writerow([id_str, enter_str, exit_str, age, gender])

    print(f"Successfully generated {NUM_RECORDS} records in '{filename}'")

if __name__ == "__main__":
    FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_sample_data.csv")

    create_sample_data(FILE_NAME)