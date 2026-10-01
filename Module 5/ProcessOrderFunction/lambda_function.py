import json
import boto3
import time
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Orders")


def lambda_handler(event, context):
    order_id = event.get("orderId")

    if not order_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "orderId is required"})
        }

    time.sleep(5)

    table.update_item(
        Key={"orderId": order_id},
        UpdateExpression="SET #status = :status, completedAt = :completed",
        ExpressionAttributeNames={"#status": "status"},
        ExpressionAttributeValues={
            ":status": "COMPLETED",
            ":completed": datetime.now(timezone.utc).isoformat()
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "orderId": order_id,
            "status": "COMPLETED"
        })
    }
