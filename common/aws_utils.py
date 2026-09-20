import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# Initialize the S3 client
def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

def upload_to_s3(file_path: str, s3_file_name: str) -> str:
    """
    Uploads a file to AWS S3 and returns the public URL.
    """
    bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
    
    if not bucket_name:
        print("AWS_S3_BUCKET_NAME is not set in environment variables.")
        return None

    s3_client = get_s3_client()
    
    try:
        # Upload the file
        s3_client.upload_file(file_path, bucket_name, s3_file_name)
        
        # Generate the S3 URL
        region = os.getenv('AWS_REGION', 'us-east-1')
        url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{s3_file_name}"
        return url
        
    except FileNotFoundError:
        print(f"The file {file_path} was not found")
        return None
    except NoCredentialsError:
        print("AWS Credentials not available")
        return None
    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        return None
