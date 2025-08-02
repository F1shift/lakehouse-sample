import json
import boto3
import os

REGION = os.environ["REGION"]
SOURCE_S3_BUCKET = os.environ["SOURCE_S3_BUCKET"]
SEARCH_PREFIX = os.environ["SEARCH_PREFIX"]

def lambda_handler(event, context):
    s3_client = boto3.client('s3', region_name=REGION)
    object_list = s3_client.get_paginator("list_objects_v2").paginate(Bucket=SOURCE_S3_BUCKET, Prefix=SEARCH_PREFIX)

    print(object_list)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
