import json
import boto3
import time

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Orders")


def lambda_handler(event, context):
    order_id = None

    if event.get("pathParameters"):
        order_id = event["pathParameters"].get("orderId")

    if not order_id:
        order_id = event.get("orderId")

    if not order_id:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "orderId is required"})
        }

    max_checks = 10
    wait_seconds = 2

    for _ in range(max_checks):
        response = table.get_item(Key={"orderId": order_id})
        order = response.get("Item")

        if not order:
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "Order not found"})
            }

        if order.get("status") != "PENDING":
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "orderId": order["orderId"],
                    "status": order["status"],
                    "createdAt": order.get("createdAt"),
                    "completedAt": order.get("completedAt")
                })
            }

        time.sleep(wait_seconds)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "orderId": order["orderId"],
            "status": order["status"],
            "message": "Still processing"
        })
    }
