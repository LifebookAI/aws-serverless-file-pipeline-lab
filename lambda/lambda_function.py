import json
import os
import time
import urllib.parse
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    processed = []

    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])
        size = record["s3"]["object"].get("size", 0)
        event_time = record.get("eventTime")

        item = {
            "file_id": key,
            "bucket": bucket,
            "object_key": key,
            "size_bytes": int(size),
            "event_time": event_time,
            "processed_at_epoch": int(time.time()),
            "status": "processed"
        }

        table.put_item(Item=item)
        print("Wrote metadata item:", json.dumps(item))

        processed.append(item)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "File metadata processed successfully",
            "processed_count": len(processed)
        })
    }
