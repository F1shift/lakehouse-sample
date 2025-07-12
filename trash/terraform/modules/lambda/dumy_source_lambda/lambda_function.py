import json
import logging
import boto3
imoprt os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DELIVERY_STREAM_NAME = os.environ("DELIVERY_STREAM_NAME")

def lambda_handler(event, context):

    client = boto3.client('firehose')
    DeliveryStreamName
    response = client.put_record_batch(
        DeliveryStreamName='string',
        Records=[
            
        ]
    )   
    return {
        'statusCode': 201,
        'body': json.dumps('Hello from Lambda!')
    }







