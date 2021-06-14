import logging 
import boto3 
from botocore.exceptions import ClientError
from botocore.config import Config
import requests

ACCESS_KEY = "AKIA3PFOCQDFKAKHBPBZ"
SECRET_KEY = "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"
BUCKET_NAME = "jobsbucket"
REGION_NAME = "eu-north-1"


def create_presigned_post(bucket_name=None, object_name=None,
                          fields=None, conditions=None, expiration=3600):
    

    # Generate a presigned S3 POST URL
    s3_client = boto3.client("s3", config=Config(signature_version='s3v4'),
                             region_name=REGION_NAME,
                             aws_access_key_id=ACCESS_KEY,
                             aws_secret_access_key=SECRET_KEY)
    try:
        response = s3_client.generate_presigned_post(Bucket=BUCKET_NAME,
                                                     Key="OBJECT_PATH",
                                                     ExpiresIn=3600)
    except ClientError as e:
        return None

    # The response contains the presigned URL and required fields
    return response


resp = create_presigned_post()

# Extract the URL and other fields from the response
post_url = resp['url']
data = resp['fields']
key = data['key']

# Upload the file using requests module
response = requests.post(url=post_url, data=data,
                         files={'file': open(r'C:\Users\212757215\Desktop\Dockerfile.txt', 'rb')})

print(response)

