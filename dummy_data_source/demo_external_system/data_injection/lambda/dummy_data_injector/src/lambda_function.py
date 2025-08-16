import json
import logging
import os
import datetime
import boto3
from firehose import FirehoseClient
import csv

# リモートデバッグする際のみ有効にする。
# AWS環境にデプロイする際に無効化すること。
import ptvsd
ptvsd.enable_attach(address=('0.0.0.0', 9999), redirect_output=True)
ptvsd.wait_for_attach()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SOURCE_S3_BUCKET_NAME = os.environ["SOURCE_S3_BUCKET_NAME"]
SOURCE_S3_PREFIX = os.environ["SOURCE_S3_PREFIX"]
DELIVERY_STREAM_NAME = os.environ["DELIVERY_STREAM_NAME"]

def lambda_handler(event, context):
    """
    S3から特定の時刻のサンプルデータを取得し、日付を現在の日付に書き換えてFirehoseに送信するLambda関数。
    """
    # 1. Lambdaがトリガーされた実行時刻を特定する (JST)
    jst = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    now = datetime.datetime.now(jst)
    logger.info(f"Execution time (JST): {now.isoformat()}")

    # 2. S3から対応する時刻のサンプルデータファイルを取得
    # ファイル名は 'sample_data_2025-01-01T<hh>_<mm>.csv' 形式
    target_filename = f"sample_data_2025-01-01T{now.strftime('%H_%M')}.csv"
    # S3のキーは '/' で結合する
    s3_key = f"{SOURCE_S3_PREFIX}/{target_filename}"

    # デバッグ用
    s3_key = f"{SOURCE_S3_PREFIX}/sample_data_2025-01-01T10_00.csv"

    logger.info(f"Attempting to get object from S3: Bucket={SOURCE_S3_BUCKET_NAME}, Key={s3_key}")

    s3_client = boto3.client('s3')
    try:
        response = s3_client.get_object(Bucket=SOURCE_S3_BUCKET_NAME, Key=s3_key)
        csv_content = response['Body'].read().decode('utf-8')
        logger.info(f"Successfully retrieved {s3_key} from S3.")
    except s3_client.exceptions.NoSuchKey:
        logger.warning(f"Source file not found in S3: {s3_key}")
        return {
            'statusCode': 404,
            'body': json.dumps(f'Source file not found: {s3_key}')
        }
    except Exception as e:
        logger.error(f"Error getting object from S3: {e}")
        raise e

    # 3. 取得したCSVを読み取る (DictReaderを使用)
    try:
        csv_dict_reader = csv.DictReader(csv_content.splitlines())
        records = list(csv_dict_reader)
        logger.info(f"Read {len(records)} records from the CSV file.")
    except Exception as e:
        logger.error(f"Error reading CSV content: {e}")
        raise e

    # 4. レコードの日付を現在の日付に書き換える (DictReaderからの辞書を使用)
    firehose_records = []
    
    for record in records:
        try:
            original_timestamp_str = record['timestamp']
            original_dt = datetime.datetime.fromisoformat(original_timestamp_str)
            
            # 日付部分を現在の日付に、時刻部分は元のデータを維持
            new_dt = original_dt.replace(year=now.year, month=now.month, day=now.day)
            
            firehose_record = record.copy()
            firehose_record['timestamp'] = new_dt.isoformat()
            
            firehose_records.append(firehose_record)
        except (KeyError, ValueError) as e:
            logger.warning(f"Skipping malformed record: {record}. Error: {e}")
            continue

    # 5. Firehoseストリームにレコードを送信する
    if not firehose_records:
        logger.info("No valid records to send to Firehose.")
        return {
            'statusCode': 200,
            'body': json.dumps('No valid data to process.')
        }

    logger.info(f"Sending {len(firehose_records)} records to Firehose stream: {DELIVERY_STREAM_NAME}")
    
    firehose_client = FirehoseClient(DELIVERY_STREAM_NAME)
    success = firehose_client.put_record_batch(firehose_records)
    
    if success:
        logger.info("Successfully sent records to Firehose.")
        return {
            'statusCode': 200,
            'body': json.dumps('Successfully processed and sent data to Firehose.')
        }
    else:
        logger.error("Failed to send records to Firehose.")
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to send data to Firehose.')
        }