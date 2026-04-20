import json
import uuid
import boto3
import os

ACCESS_KEY = os.environ["ACCESS_KEY"]
SECRET_KEY = os.environ["SECRET_KEY"]
UPLOAD_BUCKET = os.environ["UPLOAD_BUCKET"]

s3 = boto3.client(
    "s3",
    endpoint_url="https://storage.yandexcloud.net",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

def handler(event, context):
    task_id = str(uuid.uuid4())
    object_key = f"tasks/{task_id}.txt"

    upload_url = s3.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": UPLOAD_BUCKET,
            "Key": object_key,
        },
        ExpiresIn=3600,
    )

    body = {
        "task_id": task_id,
        "object_key": object_key,
        "upload_url": upload_url,
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }