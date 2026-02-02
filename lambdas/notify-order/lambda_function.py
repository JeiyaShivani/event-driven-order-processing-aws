import json

def lambda_handler(event, context):
    print("✅ Order created successfully:", json.dumps(event))
    return {
        "message": "Notification step completed",
        "details": event
    }

