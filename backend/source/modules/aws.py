import boto3
from starlette.config import Config
config = Config(".env")

access_key = config("AWS_ACCESS_KEY_ID", cast=str, default="")
secret_key = config("AWS_SECRET_ACCESS_KEY", cast=str, default="")

region = config("AWS_S3_REGION", cast=str, default="")


s3_client = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)
