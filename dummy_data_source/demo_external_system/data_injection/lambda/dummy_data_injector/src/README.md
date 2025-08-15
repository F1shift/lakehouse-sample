# 目次

- [目次](#目次)
- [本lambda関数について](#本lambda関数について)
  - [概要](#概要)
  - [Lambdaのランタイム](#lambdaのランタイム)
  - [環境変数](#環境変数)
  - [使用可能なpipパッケージ](#使用可能なpipパッケージ)
- [自作Pythonモジュール説明](#自作pythonモジュール説明)
  - [firehose.py](#firehosepy)
    - [概要](#概要-1)
    - [`FirehoseClient` クラス](#firehoseclient-クラス)
      - [初期化](#初期化)
      - [メソッド](#メソッド)
        - [`put_record(self, data: Dict[str, Any]) -> bool:`](#put_recordself-data-dictstr-any---bool)
        - [`put_record_batch(self, data_list: List[Dict[str, Any]]) -> bool:`](#put_record_batchself-data_list-listdictstr-any---bool)
      - [使い方](#使い方)
        - [1. `FirehoseClient` のインポートと初期化](#1-firehoseclient-のインポートと初期化)
        - [2. 単一レコードの送信](#2-単一レコードの送信)
        - [3. 複数レコードのバッチ送信](#3-複数レコードのバッチ送信)
  - [lambda\_function.py](#lambda_functionpy)
    - [概要](#概要-2)
    - [関数](#関数)
      - [`lambda_handler(event, context):`](#lambda_handlerevent-context)


# 本lambda関数について

## 概要

S3バケットに予め`sample_data_2025-01-01T<hh>_<mm>.csv`という名前の入退店データのサンプルデータファイルが配置されている。
サンプルデータファイルは分単位で区切られている。ファイル内容は`dummy_data_source/demo_external_system/sample_data/03_split_data/README.md`を参照すること。

Lambda実行時、以下処理で実施する。

1. Lambdaがトリガーされた実行時刻を特定する。
2. トリガーされた実行時刻と同じ時刻に実行されたサンプルデータファイル`sample_data_2025-01-01T<hh>_<mm>.csv`をS3から取得する。
3. 取得したCSVを読み取る。
4. 読み取ったレコードの日付部分を現在の日付に書き換える。`sample_data_2025-01-01T<hh>_<mm>.csv`　→　`sample_data_<yyyy>-<mm>-<dd>T<hh>_<mm>.csv`
5. 日付が書き換えられたレコードをKinesis Firehose ストリームに送信する。

## Lambdaのランタイム

python3.12

## 環境変数

|変数名|説明|
|...|...|
|SOURCE_S3_BUCKET_NAME|サンプルデータファイルが配置されたS3バケット|
|SOURCE_S3_PREFIX|サンプルデータファイルを検索する際に使用するプレフィクス|
|DELIVERY_STREAM_NAME|送信先のKinesis Firehose ストリーム名|

## 使用可能なpipパッケージ

以下を参照

```bash
dummy_data_source/demo_external_system/data_injection/lambda/dummy_data_injector/src/requirements.txt
```

# 自作Pythonモジュール説明

## firehose.py

### 概要

`firehose.py` は、AWS Kinesis Data Firehose にデータを送信するための Python クライアントモジュールです。
このモジュールは `boto3` ライブラリを使用しており、単一レコードの送信とバッチでの複数レコード送信をサポートします。

### `FirehoseClient` クラス

AWS Firehose へのデータ送信を管理するクライアントクラスです。

#### 初期化

```python
def __init__(self, stream_name: str, region_name: str = 'ap-northeast-1'):
```

`FirehoseClient` のインスタンスを初期化します。

**引数:**

*   `stream_name` (str): 送信先の Firehose デリバリーストリーム名。
*   `region_name` (str, optional): AWS リージョン名。デフォルトは `'ap-northeast-1'` です。

#### メソッド

##### `put_record(self, data: Dict[str, Any]) -> bool:`

単一の JSON レコードを Firehose に送信します。

**引数:**

*   `data` (Dict[str, Any]): 送信する JSON データ（辞書形式）。

**戻り値:**

*   `bool`: 送信に成功した場合は `True`、失敗した場合は `False` を返します。

##### `put_record_batch(self, data_list: List[Dict[str, Any]]) -> bool:`

複数の JSON レコードをバッチで Firehose に送信します。
最大500レコードずつのバッチに自動的に分割して送信します。

**引数:**

*   `data_list` (List[Dict[str, Any]]): 送信する JSON データのリスト。

**戻り値:**

*   `bool`: すべてのバッチ送信に成功した場合は `True`、いずれかが失敗した場合は `False` を返します。

#### 使い方

##### 1. `FirehoseClient` のインポートと初期化

```python
from firehose import FirehoseClient

# Firehoseストリーム名を指定してクライアントを初期化
firehose_stream_name = 'your-firehose-stream-name'
client = FirehoseClient(stream_name=firehose_stream_name, region_name='ap-northeast-1')
```

##### 2. 単一レコードの送信

```python
# 送信するデータ
single_data = {'key1': 'value1', 'key2': 100}

# レコードを送信
success = client.put_record(single_data)

if success:
    print("レコードの送信に成功しました。")
else:
    print("レコードの送信に失敗しました。")
```

##### 3. 複数レコードのバッチ送信

```python
# 送信するデータのリスト
data_list = [
    {'id': 1, 'name': 'test1'},
    {'id': 2, 'name': 'test2'},
    {'id': 3, 'name': 'test3'}
]

# バッチでレコードを送信
success = client.put_record_batch(data_list)

if success:
    print("バッチ送信に成功しました。")
else:
    print("バッチ送信に失敗しました。")
```
## lambda_function.py

### 概要

Lambda関数のエントリポイントとメインプロセス

### 関数

#### `lambda_handler(event, context):`

Lambda関数のエントリポイント関数です。