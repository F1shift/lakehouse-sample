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
```
