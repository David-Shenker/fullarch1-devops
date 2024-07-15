import os
import subprocess
import boto3
from datetime import datetime
import tempfile

def lambda_handler(event, context):
    # MongoDB connection details
    mongo_uri = os.environ['MONGO_URI']
    mongo_db = os.environ['MONGO_DB']

    # S3 bucket details
    s3_bucket = os.environ['S3_BUCKET']
    s3 = boto3.client('s3')

    # Path to mongodump binary (adjust path as necessary)

    # Create a temporary directory to store the mongodump output
    with tempfile.TemporaryDirectory() as tmpdir:
        dump_path = os.path.join(tmpdir, 'dump')

        # Perform mongodump
        dump_command = f'mongodump --uri {mongo_uri} --db {mongo_db} -out {dump_path}'

        try:
            os.popen(dump_command)
        except subprocess.CalledProcessError as e:
            print(f"Error during mongodump: {e}")
            return {
                'statusCode': 500,
                'body': 'Error during mongodump'
            }

        # Create a zip file of the dump
        zip_file_path = os.path.join(tmpdir, f'dump_{datetime.now().strftime("%Y%m%d%H%M%S")}.zip')
        zip_command = f'zip -r {zip_file_path} {dump_path}'

        try:
            os.popen(zip_command)
        except subprocess.CalledProcessError as e:
            print(f"Error during zip creation: {e}")
            return {
                'statusCode': 500,
                'body': 'Error during zip creation'
            }

        # Upload the zip file to S3
        s3_key = os.path.basename(zip_file_path)
        try:
            s3.upload_file(zip_file_path, s3_bucket, s3_key)
        except Exception as e:
            print(f"Error during S3 upload: {e}")
            return {
                'statusCode': 500,
                'body': 'Error during S3 upload'
            }

        return {
            'statusCode': 200,
            'body': f'Successfully uploaded mongodump to s3://{s3_bucket}/{s3_key}'
        }
