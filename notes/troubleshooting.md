# Troubleshooting Notes

## Issue 1: S3 Prefix Case Sensitivity

The Lambda trigger was configured for the prefix:

uploads/

At one point, an object was uploaded outside the intended lowercase uploads/ prefix.

## Root Cause

S3 prefixes are case-sensitive. A prefix named Uploads/ is different from uploads/.

## Fix

Created and used the correct lowercase uploads/ prefix, then uploaded the test file under that path.

## Lesson

When using S3 event notification filters, prefix and suffix matching must be exact. Incorrect capitalization or object placement can prevent the Lambda trigger from running.

---

## Issue 2: S3 Folder Marker Created Metadata Item

During testing, DynamoDB showed an item for:

uploads/

with size_bytes = 0.

## Root Cause

When folders are created through the S3 console, S3 can create a zero-byte folder marker object. Since the Lambda trigger watched object-created events under uploads/, the folder marker also triggered the Lambda.

## Fix / Future Improvement

For this lab, the behavior was documented.

In a production version, the Lambda code should ignore folder markers or zero-byte keys ending in /.

Example logic:

if key.endswith("/") and size == 0:
    skip processing

## Lesson

Event-driven pipelines may process more object-created events than expected unless event filters and code-level validation are both considered.

---

## Validation Performed

Successful path:

S3 upload -> Lambda invocation -> DynamoDB metadata item -> CloudWatch success logs

Failure/alert path:

Manual DLQ test message -> CloudWatch alarm in ALARM -> SNS email alert -> DLQ purge -> alarm returned to OK
