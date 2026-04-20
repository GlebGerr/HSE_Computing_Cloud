import json
import boto3
import os

ACCESS_KEY = os.environ["ACCESS_KEY"]
SECRET_KEY = os.environ["SECRET_KEY"]
RESULT_BUCKET = os.environ["RESULT_BUCKET"]

s3 = boto3.client(
    "s3",
    endpoint_url="https://storage.yandexcloud.net",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

def handler(event, context):
    messages = event.get("messages", [])
    if not messages:
        return {
            "statusCode": 400,
            "body": "no messages"
        }

    results = []

    for msg in messages:
        details = msg.get("details", {})
        bucket_id = details.get("bucket_id")
        object_id = details.get("object_id")

        if not bucket_id or not object_id:
            continue

        obj = s3.get_object(Bucket=bucket_id, Key=object_id)
        content = obj["Body"].read().decode("utf-8")

        lines = len(content.splitlines())
        words = len(content.split())
        chars = len(content)

        task_id = object_id.split("/")[-1].replace(".txt", "")
        result_key = f"results/{task_id}.json"

        result_body = {
            "task_id": task_id,
            "source_object": object_id,
            "lines": lines,
            "words": words,
            "chars": chars,
        }

        s3.put_object(
            Bucket=RESULT_BUCKET,
            Key=result_key,
            Body=json.dumps(result_body, ensure_ascii=False).encode("utf-8"),
            ContentType="application/json",
        )

        results.append(result_body)

    return {
        "statusCode": 200,
        "body": json.dumps(results, ensure_ascii=False),
    }