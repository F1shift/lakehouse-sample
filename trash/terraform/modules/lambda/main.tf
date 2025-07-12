import boto3

client = boto3.client('firehose')

DeliveryStreamName

response = client.put_record_batch(
    DeliveryStreamName='string',
    Records=[
        
    ]
)   