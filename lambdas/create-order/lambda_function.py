import boto3
import uuid
from datetime import datetime
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('order')  # exact table name

def lambda_handler(event, context):
    # raise Exception("INTENTIONAL FAILURE FOR TESTING SNS")
    # Generate unique order ID
    order_id = str(uuid.uuid4())
    
    # Build item
    item = {
        'order_id': order_id,
        'status': 'CREATED',
        'created_at': datetime.utcnow().isoformat()
    }
    
    # Store in DynamoDB
    table.put_item(Item=item)
    
    # Return response
    return {
        "order_id": order_id,
        "status": "CREATED",
        "product": event["product"],
        "quantity": event["quantity"],
        "price": event["price"],
        "customer_id": event["customer_id"]
    }
