import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException

from app.settings import AWS_REGION, AWS_ACCESS_KEY, AWS_SECRET_KEY, DOMAIN_NAME

client = boto3.client(
    "ses",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)


def verify_email_func(email_address: str):
    response = client.verify_email_address(
        EmailAddress=[email_address]
    )
    return {
        "message": "Verification Email sent!",
        "response": response
    }


def send_email_via_boto(user_email: str, subject: str, body: str):
    recipient = user_email.lower().strip()
    charset = 'UTF-8'
    sender = DOMAIN_NAME
    try:
        response = client.send_email(
            Destination={
                "ToAddresses": [
                    recipient
                ]
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": charset,
                        "Data": body
                    }
                },
                "Subject": {
                    "Charset": charset,
                    "Data": subject
                }
            },
            Source=sender
        )
    except ClientError as ce:
        raise HTTPException(status_code=500, detail=str(
            ce.response["Error"]["Message"]))

    return response
