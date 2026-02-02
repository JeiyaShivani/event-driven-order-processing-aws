import json
import boto3
import os

sfn = boto3.client("stepfunctions")

# we are using env variable here which is the statemachine's arn
STATE_MACHINE_ARN = os.environ["STATE_MACHINE_ARN"]

def lambda_handler(event, context):
    body = event.get("body")
    
    if body and isinstance(body, str):
        body = json.loads(body)

    if body is None:
        body = event

    response = sfn.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        input=json.dumps(body)
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Workflow started",
            "executionArn": response["executionArn"]
        })
    }

