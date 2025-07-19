import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# CSVファイルを読み込む
df = pd.read_csv('all_sample_data.csv')

# timestampのタイムゾーン情報を削除
df['enter_timestamp'] = pd.to_datetime(df['enter_timestamp']).dt.tz_localize(None)
df['exit_timestamp'] = pd.to_datetime(df['exit_timestamp']).dt.tz_localize(None)

# グラフ1: タイムスタンプのヒストグラム
plt.figure(figsize=(10, 6))
plt.hist([df['enter_timestamp'], df['exit_timestamp']], bins=pd.date_range(start='2025-01-01T08:00:00', end='2025-01-01T21:00:00', freq='H'), label=['enter_timestamp', 'exit_timestamp'])
plt.xlabel('Timestamp')
plt.ylabel('Count')
plt.title('Timestamp Distribution')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('all_sample_data_timestamp.png')
plt.close()

# グラフ2: 年齢のヒストグラム
plt.figure(figsize=(10, 6))
plt.hist(df['age'], bins=range(0, 101, 10), edgecolor='black')
plt.xlabel('Age')
plt.ylabel('Count')
plt.title('Age Distribution')
plt.xticks(range(0, 101, 10))
plt.grid(axis='y', linestyle='--')
plt.savefig('all_sample_data_age.png')
plt.close()

# グラフ3: 性別のヒストグラム
plt.figure(figsize=(6, 4))
df['gender'].value_counts().plot(kind='bar', edgecolor='black')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.title('Gender Distribution')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--')
plt.tight_layout()
plt.savefig('all_sample_data_gender.png')
plt.close()

print("グラフが正常に作成されました。")
