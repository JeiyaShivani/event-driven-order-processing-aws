import json
import boto3
import os
import time

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = "order"  # your table name

table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    # SQS sends records in event["Records"]
    print("RAW EVENT:", json.dumps(event))

    for record in event["Records"]:
        body = record["body"]
        message = json.loads(body)

        order_id = message["order_id"]
        product = message["product"]
        quantity = message["quantity"]

        print(f"Processing order_id={order_id}, product={product}, quantity={quantity}")

        # simulate processing time (like payment/inventory/email etc)
        time.sleep(1)

        # Update DynamoDB status
        table.update_item(
            Key={"order_id": order_id},
            UpdateExpression="SET #s = :newStatus",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":newStatus": "PROCESSED"}
        )

        print(f"Order {order_id} updated to PROCESSED")

    return {"message": "Processed batch successfully"}
