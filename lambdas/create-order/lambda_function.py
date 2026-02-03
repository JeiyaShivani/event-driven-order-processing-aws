import boto3
import uuid
from datetime import datetime
from botocore.exceptions import ClientError
from time import time

dynamodb = boto3.resource("dynamodb")
orders_table = dynamodb.Table("order")
idempotency_table = dynamodb.Table("OrderIdempotencyTable")

def lambda_handler(event, context):
    idempotency_key = event["idempotency_key"]

    try:
        # Create new order
        order_id = str(uuid.uuid4())
        ttl_seconds = int(time()) + (24 * 60 * 60)

        idempotency_table.put_item(
            Item={
                "idempotency_key": idempotency_key,
                "order_id": order_id,
                "status": "CREATED",
                "created_at": datetime.utcnow().isoformat(),
                "ttl": ttl_seconds
            },
            ConditionExpression="attribute_not_exists(idempotency_key)"
        )

        # Store actual order
        orders_table.put_item(
            Item={
                "order_id": order_id,
                "product": event["product"],
                "quantity": event["quantity"],
                "price": event["price"],
                "customer_id": event["customer_id"],
                "status": "CREATED",
                "created_at": datetime.utcnow().isoformat()
            }
        )

        return {
            "order_id": order_id,
            "status": "CREATED",
            "idempotent": False
        }

    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            # Duplicate request → fetch existing order
            response = idempotency_table.get_item(
                Key={"idempotency_key": idempotency_key}
            )

            return {
                "order_id": response["Item"]["order_id"],
                "status": response["Item"]["status"],
                "idempotent": True
            }

        else:
            raise
