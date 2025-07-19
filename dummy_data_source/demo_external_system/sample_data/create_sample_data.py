#%%
"""
# ファイルフォーマット要件

- ファイル形式: CSV
- ファイル名: all_sample_data.csv
- カラム:
  
| カラム          |                          | 型       | 説明                 |
| --------------- | ------------------------ | -------- | -------------------- |
| id              | 識別ID                   | str      | uuid4の文字列        |
| enter_timestamp | 境界線の内側に入った時刻 | datetime | yyyy-mm-ddTHH:MM:SSZ+0900 |
| exit_timestamp  | 境界線の外側に出た時刻   | datetime | yyyy-mm-ddTHH:MM:SSZ+0900 |
| age             | 年齢                     | int      | 0~                   |
| gender          | 性別                     | str      | male、female         |

# データ内容要件

- 100000件のデータを生成する
- 100000件のデータをCSV形式で保存する
- データをenter_timestampを昇順で並ぶこと
- enter_timestamp、exit_timestampの日付部分は「2025-01-01」にする
- enter_timestamp、exit_timestampの時刻部分の最小値は「00:08:00Z+0900」、最大値は「21:00:00Z+0900」にする
- exit_timestampは必ずenter_timestampよりも後になる
- enter_timestampとexit_timestampの間隔45分以下になる
- enter_timestampとexit_timestampの間隔はランダムに生成する
- enter_timestampとexit_timestampの間隔はカイ二乗分布に従い、平均値5、自由度10のカイ二乗分布に従う
- ageは「0~100」の範囲でランダムに生成する
- ageはカイ二乗分布に従い、平均値20、自由度20のカイ二乗分布に従う
- genderは「male」「female」のいずれかでランダムに生成する

# データ生成方法

- create_sample_data.pyを実行することでsample_data.csvが生成される

```bash
python create_sample_data.py

# インストールしているライブラリ
@dummy_data_source/demo_external_system/sample_data/requirements.txt に参照すること。
必要であればpipパッケージをインストールしてrequirements.txtを更新してください
```
"""
#%%
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
        
        records = []
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
            records.append([id_str, enter_str, exit_str, age, gender])

        # Sort records by enter_timestamp
        records.sort(key=lambda x: datetime.fromisoformat(x[1]))
        writer.writerows(records)

    print(f"Successfully generated {NUM_RECORDS} records in '{filename}'")

FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_sample_data.csv")

create_sample_data(FILE_NAME)
