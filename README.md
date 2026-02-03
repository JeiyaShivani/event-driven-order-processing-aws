## Event-Driven Order Processing System on AWS

Traditional synchronous order systems fail silently and are hard to monitor.
This project demonstrates a resilient, event-driven order processing pipeline with centralized failure alerting.

## Architecture
<img width="1302" height="600" alt="image" src="https://github.com/user-attachments/assets/3beb65ab-1ce1-4bdb-a229-9a95a16392f6" />

## Architecture Overview

This system implements a serverless, event-driven order processing workflow using AWS managed services.

The request flow is as follows:

1. Client sends an order request via API Gateway.
2. API Gateway triggers StartWorkflowLambda which then triggers AWS Step Functions state machine.
3. Step Functions orchestrates multiple Lambda functions:
   - ValidateOrderLambda validates incoming order data.
   - CreateOrderLambda creates the order and returns an order ID.
4. On success, the order is pushed to an SQS queue for downstream processing.
5. On failure, Step Functions catches the error and publishes an alert to SNS.
6. SNS triggers AlertHandlerLambda, which logs the failure and sends real-time notifications (Slack).
7. NotifyOrderLambda handles post-processing notifications.
8. There is another lambda which is called ProcessOrderWorkerLambda.

The architecture is designed to be fault-tolerant, observable, and easily extensible.


## Services used:
AWS API Gateway

AWS DynamoDB

AWS Step Functions

AWS Lambda

Amazon SQS

Amazon SNS

Slack Webhooks

CloudWatch


## Design Decisions
- Workflow orchestration using AWS Step Functions
- Asynchronous processing using SQS
- Centralized failure handling and alerting
- Idempotent order creation using TTL-based locking,24 hours is the time to live.

### 1. Why AWS Step Functions?
Step Functions is used as the orchestration layer instead of chaining Lambdas manually.
Reasons:
- Clear visual workflow for debugging and monitoring
- Native retry, error handling, and state transitions
This makes the system easier to scale, and maintain.

### 2. Why Multiple Lambdas Instead of One?
Each Lambda has a single responsibility:
- ValidateOrderLambda : input validation
- CreateOrderLambda : order creation logic
- NotifyOrderLambda : notification handling
- AlertHandlerLambda : failure logging and alerting

### 3. Why Centralized Error Handling via Step Functions?
Errors are intentionally handled at the Step Functions level using `Catch` blocks instead of inside each Lambda.
- Consistent failure handling across the workflow
- Failures are routed to SNS, which fans out alerts to downstream systems.


### 4. Why SNS + Lambda for Alerts?
Instead of directly calling Slack or email from Step Functions
- SNS publishes failure events
- AlertHandlerLambda subscribes to SNS
- AlertHandlerLambda sends Slack notifications and logs to CloudWatch
This allows adding more alerting targets (email, PagerDuty) without changing the workflow.

