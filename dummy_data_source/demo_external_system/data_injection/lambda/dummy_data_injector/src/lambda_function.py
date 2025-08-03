import json
import logging
import os
import uuid
import datetime
import boto3
from firehose import FirehoseClient
import itertools

# リモートデバッグする際のみ有効にする。
# AWS環境にデプロイする際に無効化すること。
# import ptvsd
# ptvsd.enable_attach(address=('0.0.0.0', 9999), redirect_output=True)
# ptvsd.wait_for_attach()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SOURCE_S3_BUCKET_NAME = os.environ["SOURCE_S3_BUCKET_NAME"]
SOURCE_S3_PREFIX = os.environ["SOURCE_S3_PREFIX"]
DELIVERY_STREAM_NAME = os.environ["DELIVERY_STREAM_NAME"]

def lambda_handler(event, context):
    pager = boto3.client('s3').get_paginator('list_objects_v2').paginate(Bucket=SOURCE_S3_BUCKET_NAME)
    source_data_objects = []
    for page in pager:
        source_data_objects.extend(page['Contents'])
    # datas = [
    #     {
    #         "human_id": str(uuid.uuid4()),
    #         "timestamp": str(datetime.datetime.now().isoformat()),
    #         "direction": True,
    #         "guessed_age": 20,
    #         "guessed_gender": False,
    #     }
    # ]
    # logger.info(f"DELIVERY_STREAM_NAME:{DELIVERY_STREAM_NAME}")
    # logger.info(datas)
    # client = FirehoseClient(DELIVERY_STREAM_NAME)
    # response = client.put_record_batch(datas)
    return {
        'statusCode': 200,
        'body': json.dumps('Done!')
    }