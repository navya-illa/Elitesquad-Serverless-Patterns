import json
import boto3
import uuid
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")
lambda_client = boto3.client("lambda")
table = dynamodb.Table("Orders")


def lambda_handler(event, context):
    order_id = str(uuid.uuid4())

    order = {
        "orderId": order_id,
        "status": "PENDING",
        "createdAt": datetime.now(timezone.utc).isoformat()
    }

    table.put_item(Item=order)

    lambda_client.invoke(
        FunctionName="ProcessOrderFunction",
        InvocationType="Event",
        Payload=json.dumps({"orderId": order_id}).encode("utf-8")
    )

    return {
        "statusCode": 202,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "orderId": order_id,
            "status": "PENDING",
            "message": "Order accepted for processing"
        })
    }
