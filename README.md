# AWS Serverless File Processing Pipeline Lab

## Overview

This project documents a hands-on AWS serverless lab where I built, tested, monitored, and documented an event-driven file processing pipeline.

The pipeline uses S3 for file uploads, Lambda for event-driven processing, DynamoDB for metadata storage, SQS as a dead-letter queue, SNS for alert notifications, IAM least-privilege permissions, and CloudWatch for logs, metrics, and alarms.

The goal of this lab was to understand how AWS serverless services work together in a production-style event-driven architecture.

---

## Architecture

User uploads file -> S3 bucket -> S3 event notification -> Lambda processor -> DynamoDB metadata table

Failure/operations path:

Lambda failure or failed processing event -> SQS DLQ -> CloudWatch alarm -> SNS email alert

---

## AWS Services Used

- Amazon S3
- AWS Lambda
- Amazon DynamoDB
- Amazon SQS
- Amazon SNS
- Amazon CloudWatch
- AWS IAM

---

## Pipeline Design

| Component | Purpose |
|---|---|
| S3 upload bucket | Stores uploaded files and emits object-created events |
| Lambda processor | Processes S3 events and writes metadata |
| DynamoDB table | Stores structured file metadata |
| SQS DLQ | Captures failed processing events |
| SNS topic | Sends alert notifications |
| CloudWatch | Provides logs, metrics, and alarms |
| IAM role | Grants least-privilege Lambda permissions |

---

## S3 Upload Bucket

The S3 bucket is the entry point for the pipeline. It was configured as private with public access blocked and default encryption enabled.

Evidence:

- [S3 upload bucket created](screenshots/01-s3-upload-bucket-created.png)
- [S3 block public access enabled](screenshots/02-s3-block-public-access.png)
- [S3 default encryption enabled](screenshots/03-s3-default-encryption.png)

---

## DynamoDB Metadata Table

DynamoDB stores metadata for uploaded files, including file ID, bucket name, object key, file size, event time, processed timestamp, and status.

Evidence:

- [DynamoDB table created](screenshots/04-dynamodb-table-created.png)
- [DynamoDB metadata item created](screenshots/14-dynamodb-metadata-item-created.png)

---

## Dead-Letter Queue and Alerts

An SQS dead-letter queue was created to capture failed processing events. A CloudWatch alarm monitors visible messages in the DLQ and sends notifications through SNS.

Evidence:

- [SQS DLQ created](screenshots/05-sqs-dlq-created.png)
- [SNS alert topic created](screenshots/06-sns-alert-topic-created.png)
- [SNS email subscription confirmed](screenshots/07-sns-email-subscription-confirmed.png)
- [CloudWatch DLQ alarm created](screenshots/16-cloudwatch-dlq-alarm-created.png)
- [SQS DLQ test message sent](screenshots/17-sqs-dlq-test-message-sent.png)
- [CloudWatch alarm in ALARM state](screenshots/18-cloudwatch-dlq-alarm-in-alarm.png)
- [SNS email alert received](screenshots/19-sns-email-alert-received.png)
- [CloudWatch alarm returned to OK](screenshots/20-cloudwatch-dlq-alarm-back-to-ok.png)

---

## Lambda Processor

The Lambda function receives S3 object-created events, extracts file metadata, writes the metadata item to DynamoDB, and logs the processing result to CloudWatch.

Key behavior:

- Reads S3 event records
- Extracts bucket name, object key, file size, and event time
- Writes metadata to DynamoDB
- Logs success to CloudWatch

Evidence:

- [Lambda execution role created](screenshots/08-lambda-execution-role-created.png)
- [Lambda least-privilege inline policy added](screenshots/09-lambda-role-inline-policy-added.png)
- [Lambda function code deployed](screenshots/10-lambda-function-code-deployed.png)
- [Lambda environment variable configured](screenshots/11-lambda-environment-variable.png)
- [S3 trigger added to Lambda](screenshots/12-s3-trigger-added-to-lambda.png)
- [CloudWatch Lambda success logs](screenshots/15-cloudwatch-lambda-success-logs.png)
- [Lambda monitoring metrics](screenshots/15a-lambda-monitoring-metrics.png)

---

## IAM Least Privilege

The Lambda function uses a dedicated execution role. It has CloudWatch Logs permissions, plus a custom inline policy allowing only the specific S3 and DynamoDB actions required for this lab.

Permissions were scoped to:

- Read objects from the specific S3 upload bucket
- Write items to the specific DynamoDB metadata table
- Write Lambda logs to CloudWatch

This avoids broad permissions such as AdministratorAccess or full-account S3/DynamoDB access.

---

## End-to-End Validation

The pipeline was tested by uploading a file under the S3 uploads/ prefix.

Validation result:

- S3 object upload succeeded
- S3 event triggered Lambda
- Lambda wrote metadata to DynamoDB
- CloudWatch logs confirmed processing
- DLQ alarm path was manually tested
- SNS email alert was received

Evidence:

- [S3 test file uploaded](screenshots/13-s3-test-file-uploaded.png)
- [DynamoDB metadata item created](screenshots/14-dynamodb-metadata-item-created.png)
- [CloudWatch Lambda success logs](screenshots/15-cloudwatch-lambda-success-logs.png)

---

## Troubleshooting / Learning Note

During testing, an S3 folder marker object under uploads/ also generated a metadata record with a size of 0 bytes. This happened because S3 prefixes are represented as objects when folders are created through the console.

This was useful because it showed that event-driven pipelines may process more object-created events than expected unless filters or code-level validation are used.

Future improvement: ignore folder marker objects or zero-byte keys ending in /.

---

## Cost Control and Cleanup

After validation, resources should be cleaned up to avoid unnecessary charges.

Main cleanup targets:

- S3 objects and bucket
- Lambda function
- DynamoDB table
- SQS DLQ
- SNS topic/subscription
- CloudWatch alarm/log group
- IAM role and inline policy

---

## What I Learned

- How S3 event notifications trigger Lambda
- How Lambda processes event payloads
- How to store structured metadata in DynamoDB
- How to configure IAM least privilege for Lambda
- How to use CloudWatch logs and metrics for validation
- How DLQs support failure recovery
- How SNS alerts support operational visibility
- How to test success and failure paths in a serverless pipeline

---

## Future Improvements

- Rebuild the pipeline using Terraform
- Add architecture diagram SVG/PNG
- Add file type validation
- Ignore zero-byte folder marker objects
- Add Lambda unit tests
- Add structured JSON logging
- Add retry/reprocessing workflow from DLQ
- Add S3 lifecycle policy for uploaded files
