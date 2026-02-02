import json
import datetime
import os
import urllib3

http = urllib3.PoolManager()
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def lambda_handler(event, context):
    record = event["Records"][0]
    message = json.loads(record["Sns"]["Message"])

    alert = {
        "alert_time": datetime.datetime.utcnow().isoformat(),
        "order_id": message.get("order_id"),
        "error": message.get("error"),
        "source": "order-processing-workflow"
    }
    print("ALERT RECEIVED:")
    print(json.dumps(alert, indent=2))

    
    slack_message = {
        "text": f"*Order Processing Alert*\nOrder ID: {alert['order_id']}\nError: {alert['error']}\nTime: {alert['alert_time']}"
    }

    try:
        response = http.request(
            "POST",
            SLACK_WEBHOOK_URL,
            body=json.dumps(slack_message).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        print("Slack response status:", response.status)
    except Exception as e:
        print("Failed to send Slack notification:", str(e))

    return {"status": "logged and notified"}

