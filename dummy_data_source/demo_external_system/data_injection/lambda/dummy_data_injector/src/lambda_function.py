import json
import logging
import os
import uuid
import datetime
from firehose import FirehoseClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SOURCE_S3_BUCKET_NAME = os.environ["SOURCE_S3_BUCKET_NAME"]
SOURCE_S3_PREFIX = os.environ["SOURCE_S3_PREFIX"]
DELIVERY_STREAM_NAME = os.environ["DELIVERY_STREAM_NAME"]

def lambda_handler(event, context):
    datas = [
        {
            "human_id": str(uuid.uuid4()),
            "timestamp": str(datetime.datetime.now().isoformat()),
            "direction": True,
            "guessed_age": 20,
            "guessed_gender": False,
        }
    ]
    logger.info(f"DELIVERY_STREAM_NAME:{DELIVERY_STREAM_NAME}")
    logger.info(datas)
    client = FirehoseClient(DELIVERY_STREAM_NAME)
    response = client.put_record_batch(datas)
    return {
        'statusCode': 200,
        'body': json.dumps('Done!')
    }