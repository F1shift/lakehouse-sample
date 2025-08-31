import pandas as pd
import os

# 入力ファイルのパス
input_file = os.path.join(os.path.dirname(__file__), '../01_create_data/output/all_sample_data.csv')

# 出力ディレクトリのパス
output_dir = os.path.join(os.path.dirname(__file__), 'output')

# 出力ディレクトリが存在しない場合は作成
os.makedirs(output_dir, exist_ok=True)

# CSVファイルを読み込む
df = pd.read_csv(input_file)

# タイムスタンプのフォーマットを定義
date_format = '%Y-%m-%dT%H:%M:%S%z'

# enter_timestampとexit_timestampをdatetime型に変換
df['enter_timestamp'] = pd.to_datetime(df['enter_timestamp'], format="ISO8601")
df['exit_timestamp'] = pd.to_datetime(df['exit_timestamp'], format="ISO8601")

# データを整形
enter_df = df[['id', 'enter_timestamp', 'age', 'gender']].copy()
enter_df.rename(columns={'enter_timestamp': 'timestamp'}, inplace=True)
enter_df['direction'] = 1

exit_df = df[['id', 'exit_timestamp', 'age', 'gender']].copy()
exit_df.rename(columns={'exit_timestamp': 'timestamp'}, inplace=True)
exit_df['direction'] = -1

# データを結合
all_df = pd.concat([enter_df, exit_df])

# shop_idカラムを追加
all_df['shop_id'] = "0123456"

# タイムスタンプでソート
all_df.sort_values('timestamp', inplace=True)

# タイムスタンプで分単位にグループ化
# timestamp列を分単位で切り捨てた値('min'は分を意味します)でグループ化します。
for group_timestamp, group in all_df.groupby(all_df['timestamp'].dt.floor('min')):
    # グループのキーとなっているタイムスタンプから直接ファイル名を生成します。
    output_filename = group_timestamp.strftime('sample_data_%Y-%m-%dT%H_%M.csv')
    output_path = os.path.join(output_dir, output_filename)

    # データをCSVファイルとして書き出す
    group.to_csv(output_path, index=False, date_format=date_format)
