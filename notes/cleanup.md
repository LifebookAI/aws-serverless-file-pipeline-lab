# Cleanup Notes

After validation and screenshots, Lab 2 resources should be deleted to avoid unnecessary AWS charges and account clutter.

## Recommended Cleanup Order

1. Delete test objects from the S3 bucket.
2. Delete the S3 bucket.
3. Delete the Lambda function.
4. Delete the DynamoDB table.
5. Delete the SQS DLQ.
6. Delete the CloudWatch alarm.
7. Delete the SNS subscription.
8. Delete the SNS topic.
9. Delete the Lambda CloudWatch log group.
10. Delete the Lambda IAM role and inline policy.

## Why This Order

The Lambda trigger depends on the S3 bucket and Lambda function.

The CloudWatch alarm depends on the SQS DLQ metric and SNS topic action.

The IAM role should be deleted after Lambda is removed, because Lambda uses the role while it exists.

## Cost Awareness

Most resources in this lab are low cost at small scale, but cleanup is still part of professional cloud practice.

Cleaning up shows:

- Cost awareness
- Resource lifecycle discipline
- Understanding of service dependencies
- Responsible AWS account hygiene
