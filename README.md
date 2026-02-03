## Event-Driven Order Processing System on AWS

Traditional synchronous order systems fail silently and are hard to monitor.
This project demonstrates a resilient, event-driven order processing pipeline with centralized failure alerting.

## Architecture
<img width="1302" height="600" alt="image" src="https://github.com/user-attachments/assets/3beb65ab-1ce1-4bdb-a229-9a95a16392f6" />

## Architecture Overview

This system implements a serverless, event-driven order processing workflow using AWS managed services.

The request flow is as follows:

1. Client sends an order request via API Gateway.
2. API Gateway triggers an AWS Step Functions state machine.
3. Step Functions orchestrates multiple Lambda functions:
   - ValidateOrderLambda validates incoming order data.
   - CreateOrderLambda creates the order and returns an order ID.
4. On success, the order is pushed to an SQS queue for downstream processing.
5. On failure, Step Functions catches the error and publishes an alert to SNS.
6. SNS triggers AlertHandlerLambda, which logs the failure and sends real-time notifications (Slack).
7. NotifyOrderLambda handles post-processing notifications.

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
